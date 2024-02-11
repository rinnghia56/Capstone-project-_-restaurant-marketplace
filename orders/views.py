from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts
from vendor.models import Vendor
from .forms import OrderForm
from .models import Order, Payment, OrderedFood
from menu.models import FoodItem
from .utils import generate_order_number, order_total_by_vendor
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from decimal import Decimal
import simplejson as json
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
@login_required(login_url='login')
def place_order(request):
    if not 'lat_checkout' in request.POST and not 'lng_checkout' in request.POST:
        return redirect('cart')
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count < 0:
        return redirect('marketplace')
    
    vendors_ids = []
    for i in cart_items:
        if i.fooditem.vendor.id not in vendors_ids:
            vendors_ids.append(i.fooditem.vendor.id)

    latitude = request.POST['lat_checkout']
    longitude = request.POST['lng_checkout']


    pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
    pnt.srid = 4326

    vendors = Vendor.objects.filter(id__in=vendors_ids,
    ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

    subtotal = 0
    total_data = {}
    k = {}

    for i in cart_items:
        fooditem = FoodItem.objects.get(pk=i.fooditem.id, vendor_id__in=vendors_ids)
        v_id = fooditem.vendor.id
        if v_id in k:
            subtotal = k[v_id]
            subtotal += (fooditem.price * i.quantity)
            k[v_id] = subtotal
        else:
            subtotal = (fooditem.price * i.quantity)
            k[v_id] = subtotal

        for v in vendors:
            if v.id == v_id:
                if v is not None and hasattr(v, 'distance') and hasattr(v.distance, 'km'):
                    distance_restaurant = round(v.distance.km, 1)
                else:
                    distance_restaurant = 0
                total_data.update({fooditem.vendor.id: {str(subtotal): {str(distance_restaurant):str(round(distance_restaurant*0.21,1))}}})
              

    

    shipping_fees = [float(nested_value) for value in total_data.values() for inner_value in value.values() for nested_value in inner_value.values()]

    subtotal = get_cart_amounts(request)['subtotal']
    grand_total = get_cart_amounts(request)['grand_total']
    shipping_fee = 0

    for value in shipping_fees:
        shipping_fee += Decimal(str(value))
    
    grand_total += shipping_fee

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.total_shipping_fee = shipping_fee
            order.total_data = json.dumps(total_data)
            order.payment_method = request.POST['payment_method']    
            order.save()
            order.order_number = generate_order_number(order.id)
            order.vendors.add(*vendors_ids)
            order.save()
            context = {
                'order': order,
                'cart_items': cart_items,
                'subtotal':subtotal,
                'shipping_fee':shipping_fee
            }
            return render(request, 'orders/place_order.html', context)
        else:
            print(form.errors)
    return render(request, 'orders/place_order.html')

@login_required(login_url='login')
def payments(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )
        payment.save()
        # Update the order model
        order.payment = payment
        order.is_ordered = True
        order.save()
        

        # Move the cart items to ordered food model
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity
            ordered_food.save()
        # Send order confirmation email to the customer
        mail_subject = 'Thank you for ordering with us. '
        mail_template = 'orders/order_confirmation_email.html'

        ordered_food = OrderedFood.objects.filter(order=order)
        context = {
            'user':request.user,
            'order':order,
            'to_email':order.email,
            'ordered_food':ordered_food,
            'domain':get_current_site(request)
        }
        send_notification(mail_subject, mail_template, context)
        # Send order received email to the vendor
        mail_subject = 'You have received a new order.'
        mail_template = 'orders/new_order_received.html'
        to_emails = []
        for i in cart_items:
            if i.fooditem.vendor.user.email not in to_emails:
                to_emails.append(i.fooditem.vendor.user.email)

                ordered_food_to_vendor = OrderedFood.objects.filter(order=order, fooditem__vendor = i.fooditem.vendor)

                context_vendor = {
                    'order':order,
                    'to_email': i.fooditem.vendor.user.email,
                    'ordered_food_to_vendor': ordered_food_to_vendor,
                    'vendor_subtotal':order_total_by_vendor(order, i.fooditem.vendor.id)['subtotal'],
                    'vendor_grand_total':order_total_by_vendor(order, i.fooditem.vendor.id)['grand_total'],
                    'vendor_shipping_distance':order_total_by_vendor(order, i.fooditem.vendor.id)['shipping_distance'],
                    'vendor_shipping_fee':order_total_by_vendor(order, i.fooditem.vendor.id)['shipping_fee'],
                    'domain':get_current_site(request)
                }
                send_notification(mail_subject, mail_template, context_vendor)
        # Clear the cart if the payment is success
        # cart_items.delete()   
        response = {
            'order_number':order_number,
            'transaction_id': transaction_id,
        }
        return JsonResponse(response)


    
    return HttpResponse('Payment view')

def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')

    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)

        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)

        context = {
            'order':order,
            'ordered_food': ordered_food,
            'subtotal':subtotal
        }

        return render(request, 'orders/order_complete.html', context)
    except:
        return redirect('home')