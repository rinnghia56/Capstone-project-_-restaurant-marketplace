from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.db.models import Q
from django.db.models import Avg
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from datetime import date, datetime
from math import floor
import random
from random import sample
from django.core.paginator import Paginator
# Import model
from .models import Cart
from accounts.models import UserProfile,User
from vendor.models import Vendor, OpeningHour
from menu.models import Category, FoodItem, CategoryDefault, FoodImage, FoodFavorite
# Import form
from orders.models import OrderedFood
from feedback.models import Comment, Rating
from orders.forms import OrderForm
from feedback.forms import CommentForm
from .context_processors import get_cart_counter, get_cart_amounts


#  ======= View Marketplace ======= #

# View list restaurant
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        "vendors": vendors,
        "vendor_count": vendor_count
    }
    return render(request,'marketplace/list_restaurant.html', context)


# View list food
def list_food(request):
    list_food = FoodItem.objects.filter(is_available=True)
    paginator = Paginator(list_food, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj
    }
    return render(request,'marketplace/list_food.html', context)


# View list food by menu default
def list_food_by_menu_default(request, category_default_slug):
    category_default = get_object_or_404(CategoryDefault, slug=category_default_slug)
    list_food = category_default.fooditems_default.filter(is_available=True)
    paginator = Paginator(list_food, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj
    }
    return render(request,'marketplace/list_food_by_menu_default.html', context)

# View food details
def food_detail(request, food_slug):
    food = get_object_or_404(FoodItem, slug=food_slug)
    food_images = food.food_images.all()
    list_food = FoodItem.objects.exclude(id=food.id)
    list_food_same = food.category_default.fooditems_default.exclude(id=food.id).all()
    form_comment = CommentForm()
    comments = Comment.objects.filter(food_item=food).order_by('-created_at')

    list_food_suggestion = list_food.exclude(id=food.id).order_by('?')[:5]
    random_food_same = list_food_same.exclude(id=food.id).order_by('?')[:4]

    rating_value = Rating.objects.filter(user=request.user, food_item=food).first() if request.user.is_authenticated else None

    food_rating = []
    if food.rating_count > 0:
        food_rating = range(food.rating)

    context = {
        'food': food,
        'food_images': food_images,
        'random_food_same': random_food_same,
        'list_food_suggestion': list_food_suggestion,
        'form_comment': form_comment,
        'comments': comments,
        'rating_value': rating_value,
        'food_rating':food_rating
    }
        
    return render(request, 'marketplace/food_detail.html', context)

# View detail restaurant
def vendor_details(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor)
    foods = FoodItem.objects.filter(vendor=vendor, is_available=True)
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', '-from_hour')

    today = date.today().isoweekday()
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)

    context = {
        'vendor': vendor,
        'categories': categories,
        'foods': foods,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
    }

    return render(request, 'marketplace/vendor_detail.html', context)

# View detail restaurant by menu
def vendor_details_by_menu(request, vendor_slug, category_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor = vendor)
    category = Category.objects.get(vendor=vendor, slug = category_slug)
    foods = FoodItem.objects.filter(vendor=vendor, is_available=True,category=category)
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day','-from_hour')

    today = date.today().isoweekday()
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)

    context = {
        'vendor':vendor,
        'categories':categories,
        'foods':foods,
        'opening_hours':opening_hours,
        'current_opening_hours':current_opening_hours
    }

    return render(request,'marketplace/vendor_detail_by_menu.html', context)

#  ======= End view Marketplace ======= #

#  =======  Cart ======= #


# View cart
@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)

# Add product to cart
def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if request.user.role == 1:
                return JsonResponse({'status': 'Failed', 'message': 'You are a restaurant and cannot purchase products.'})
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                if fooditem.vendor.is_open() == False or fooditem.vendor.is_open() == None:
                     return JsonResponse({'status': 'Failed', 'message': 'The restaurant is closed'})
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

# Remove product from the cart
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})    

# Delete cart
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})

#  ======= End Cart ======= #  

# ======= Search food ======= #

# Search food by name
def search_food(request):
    if not 'food_name_search' in request.GET:
        return redirect('marketplace')
    else:
         food_name_search = request.GET['food_name_search']
         list_food = FoodItem.objects.filter(food_title__icontains=food_name_search, is_available=True)
         paginator = Paginator(list_food, 12)
         page_number = request.GET.get('page')
         page_obj = paginator.get_page(page_number)
         context ={
             'page_obj':page_obj
         }
         return render(request,'marketplace/list_food.html', context)

# Search food by address    
def search_address(request):
    if not 'address_search' in request.GET:
        return redirect('marketplace')
    else:
        address = request.GET['address_search']
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        radius = request.GET['radius']
        if(radius == ""):
            radius= 1000000


        # get vendor ids that has the food item the user is looking for
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
        if latitude and longitude and radius:
            pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))

            vendors = Vendor.objects.filter(is_approved=True, user__is_active=True,
            user_profile__location__distance_lte=(pnt, D(km=radius))
            ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

            for v in vendors:
                v.kms = round(v.distance.km, 1)
        vendor_count = vendors.count()
        context = {
            'vendors': vendors,
            'vendor_count': vendor_count,
            'source_location': address,
        }


        return render(request, 'marketplace/list_restaurant.html', context)

# Search food by name and address
def search_both(request):
    if not 'address_search' in request.GET:
        return redirect('marketplace')
    else:
        address = request.GET['address_search']
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        radius = request.GET['radius']
        keyword = request.GET['food_name_search']

        if(radius == ""):
            radius= 1000000

        # get vendor ids that has the food item the user is looking for
        fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)
        
        vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
        if latitude and longitude and radius:
            pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))

            vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True),
            user_profile__location__distance_lte=(pnt, D(km=radius))
            ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

            for v in vendors:
                v.kms = round(v.distance.km, 1)
        vendor_count = vendors.count()
        context = {
            'vendors': vendors,
            'vendor_count': vendor_count,
            'source_location': address,
        }
        return render(request, 'marketplace/list_restaurant.html', context)
    
# search restaurant near you
def search_location(request):
    if not 'lat' in request.GET and not 'lng' in request.GET:
        return redirect('marketplace')
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
    pnt.srid = 4326
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True,
            user_profile__location__distance_lte=(pnt, D(km=1000))
            ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")
    for v in vendors:
        v.kms = round(v.distance.km, 1)
    vendor_count = vendors.count()
    positions = []
    for vendor in vendors:
        if vendor.user_profile.latitude is not None and vendor.user_profile.longitude:
            positions.append({"latitude": vendor.user_profile.latitude, "longitude": vendor.user_profile.longitude, "address": vendor.user_profile.address,"restaurant_name":vendor.vendor_name})

    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
        'latitude':latitude,
        'longitude':longitude,
        'positions':positions
    }
    return render(request, 'marketplace/list_restaurant_by_location.html', context)

# ====== End search food ======

@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_items = [cart_item for cart_item in cart_items if cart_item.fooditem.vendor.is_open() != False and cart_item.fooditem.vendor.is_open() != None]
    cart_count = len(cart_items)
    if cart_count <= 0:
        return redirect('marketplace')

    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    context = {
        'form':form,
        'cart_items': cart_items
    }
    return render(request,'marketplace/checkout.html', context)


# Favorite
@login_required(login_url='login')
def foods_favorite(request):
    favorite_foods = FoodFavorite.objects.filter(user = request.user)
    food_tops = FoodItem.objects.order_by('-rating')
    if food_tops.count() < 5:
        highest_rated_items = food_tops
    else: 
        highest_rated_items = food_tops[:5]
    context = {
        'favorite_foods':favorite_foods,
        'highest_rated_items':highest_rated_items
    }
    return render(request, 'marketplace/favorite_food.html',context)

def get_foods_favorite(request):
    if request.user.is_authenticated:
        try:
            favorite_foods = FoodFavorite.objects.filter(user = request.user)
            id_food = favorite_foods.values_list('food_item__id', flat=True)
            return JsonResponse({'status': 'Success', 'message': 'Get foods favorite success','id_food': list(id_food)})
        except:
            return JsonResponse({'status': 'Failed', 'message': 'List food favorite empty'})
    else:
       return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

def add_food_favorite(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    food_favorite = FoodFavorite.objects.get(user=request.user, food_item=fooditem)
                    food_favorite.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Successfully remove from favorites'})
                except:
                    food_favorite = FoodFavorite.objects.create(user=request.user, food_item=fooditem)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the favorites list'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
    
def remove_food_favorite(request, food_favorite_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                food_favorite_item = FoodFavorite.objects.get(user=request.user, id=food_favorite_id)
                if food_favorite_item:
                    food_favorite_item.delete()
                    count_food = FoodFavorite.objects.filter(user=request.user).count()
                    return JsonResponse({'status': 'Success', 'message': 'Food favorite has been deleted!','count_food':count_food})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Food favorite does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})