from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .forms import VendorForm, OpeningHourForm
from accounts.forms import UserProfileForm
from menu.forms import CategoryForm, FoodItemForm, FoodImageForm
from blogs.forms import PostForm
from django.db import IntegrityError

from accounts.models import UserProfile
from .models import Vendor, OpeningHour
from menu.models import Category, FoodItem, FoodImage
from orders.models import Order, OrderedFood
from feedback.models import Comment
from blogs.models import Post
from django.template.defaultfilters import slugify


from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from django.core.paginator import Paginator
from django.db.models import Count


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    vendor = get_object_or_404(Vendor,user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vprofile')
        else:
           print(profile_form.errors)
           print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance = vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile':profile,
        'vendor':vendor
    }
    return render(request,'vendor/vprofile.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    foods = FoodItem.objects.filter(vendor=vendor)
    context = {
        'categories': categories,
        'foods':foods
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk = None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'category':category,
        'fooditems':fooditems,
    }
    return render(request,'vendor/fooditems_by_category.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if get_vendor(request).is_approved == False:
        messages.success(request,'Sorry, your restaurant has not been licensed')
        return redirect('menu_builder')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.save()
            category.slug = slugify(category_name) + '-' + str(category.id)
            category.save()
            messages.success(request,'Category added successfully')
            return redirect('menu_builder')
    else:
        form = CategoryForm()
    context = {
        'form':form,
    }
    return render(request,'vendor/add_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    if get_vendor(request).is_approved == False:
        messages.success(request,'Sorry, your restaurant has not been licensed')
        return redirect('menu_builder')
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category_desc = form.cleaned_data['description']
            category.category_name = category_name
            category.description = category_desc
            category.slug = slugify(category_name) + '-' + str(category.id)
            category.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    if get_vendor(request).is_approved == False:
        messages.success(request,'Sorry, your restaurant has not been licensed')
        return redirect('menu_builder')   
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if get_vendor(request).is_approved == False:
        messages.success(request,'Sorry, your restaurant has not been licensed')
        return redirect('menu_builder')
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.save()
            food.slug = slugify(foodtitle) + '-' + str(food.id)
            food.save()
            messages.success(request, 'Food Item added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_food.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    if get_vendor(request).is_approved == False:
        messages.success(request,'Sorry, your restaurant has not been licensed')
        return redirect('menu_builder')
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodtitle) + '-' + str(food.id)
            form.save()
            messages.success(request, 'Food Item updated successfully!')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)

    else:
        form = FoodItemForm(instance=food)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
        'food': food,
    }
    return render(request, 'vendor/edit_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, pk=None):
    if get_vendor(request).is_approved == False:
        messages.success(request,'Sorry, your restaurant has not been licensed')
        return redirect('menu_builder')
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, 'Food Item has been deleted successfully!')
    return redirect('fooditems_by_category', food.category.id)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHourForm()
    context = {
        'form': form,
        'opening_hours': opening_hours
    }
    return render(request,'vendor/opening_hours.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_opening_hours(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            try:
                hour = OpeningHour.objects.create(vendor = get_vendor(request), day = day, from_hour = from_hour, to_hour = to_hour, is_closed = is_closed)
                if hour:
                    day = OpeningHour.objects.get(id = hour.id)
                    if day.is_closed:
                         response = {'status':'success', 'id': hour.id, 'day': day.get_day_display(), 'is_closed':'Closed'}
                    else:
                         response = {'status':'success', 'id': hour.id, 'day': day.get_day_display(),'from_hour': hour.from_hour, 'to_hour': to_hour}
                return JsonResponse(response)
            except IntegrityError as e:
                response = {'status':'failed','message': from_hour + ' - ' + to_hour + ' already exists for this day!','error': str(e)}
                return JsonResponse(response)
        else:
                HttpResponse("Invalid request")

def remove_opening_hours(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour, pk = pk)
            hour.delete()
            return JsonResponse({'status':'success','id':pk})
        else:
            HttpResponse("Invalid request")

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order, fooditem__vendor=get_vendor(request))
       
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)

        context = {
            'order':order,
            'ordered_food':ordered_food,
            'subtotal': subtotal
        }
    except:
        return redirect('vendor')

    return render(request, 'vendor/order_detail.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def my_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at')
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj
    }
    return render(request, 'vendor/my_orders.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def sentiment_comment(request):
    vendor = get_vendor(request)
    fooditems = FoodItem.objects.filter(vendor=vendor)
    sentiment_counts = Comment.objects.filter(food_item__in=fooditems).values('sentiment').annotate(count=Count('sentiment'))
    
    sentiment_dict = {item['sentiment']: item['count'] for item in sentiment_counts}
    positive = sentiment_dict.get('Positive', 0)
    neutral = sentiment_dict.get('Neutral', 0)
    negative = sentiment_dict.get('Negative', 0)
    context = {
        'fooditems':fooditems,
        'positive':positive,
        'neutral':neutral,
        'negative':negative
    }

    return render(request, 'vendor/sentiment.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def view_comment_by_sentiment(request,food_id):
    if not 'type_sentiment' in request.GET:
        return redirect('vendor_sentiment_comment')
    param_value = request.GET.get('type_sentiment')
    food = FoodItem.objects.get(id=food_id)
    comments = Comment.objects.filter(food_item = food, sentiment=param_value).order_by('-created_at')
    context = {
        'food':food,
        'comments':comments,
        'param_value':param_value
    }
    print(context)
    return render(request,'vendor/comment_by_sentiment.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def view_all_comment_by_sentiment(request):
    if not 'type_sentiment' in request.GET:
        return redirect('vendor_sentiment_comment')
    param_value = request.GET.get('type_sentiment')
    foods = FoodItem.objects.filter(vendor=get_vendor(request))
    comments = Comment.objects.filter(sentiment=param_value,food_item__in=foods).order_by('-created_at')
    context = {
        'foods':foods,
        'comments':comments,
        'param_value':param_value
    }
    return render(request,'vendor/all_comment_by_sentiment.html',context)
# Food iamge

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def foodimages_by_fooditem(request, pk=None):
    food_item = get_object_or_404(FoodItem, pk=pk)
    food_images = FoodImage.objects.filter(food_item=food_item)
    context = {
        'food_item':food_item,
        'food_images':food_images,
    }
    return render(request,'vendor/foodimages_by_fooditem.html',context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_image(request,pk=None):
    if get_vendor(request).is_approved == False:
        messages.success(request,'Sorry, your restaurant has not been licensed')
        return redirect('menu_builder')
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_food = form.save(commit=False)
            image_food.food_item = food_item
            image_food.save()
            messages.success(request, 'Food Image added successfully!')
            return redirect('view_image',food_item.id)
        else:
            print(form.errors)
    else:
        form = FoodImageForm()
    context = {
        'form': form,
        'food_item':food_item
    }
    return render(request, 'vendor/add_image_food.html', context)



def delete_image(request, pk=None):
    if get_vendor(request).is_approved == False:
        messages.success(request,'Sorry, your restaurant has not been licensed')
        return redirect('menu_builder')
    image_food = get_object_or_404(FoodImage, pk=pk)
    id_food = image_food.food_item.id
    image_food.delete()
    messages.success(request, 'Food image has been deleted successfully!')
    return redirect('view_image',id_food)



# Post
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def manage_post(request):
    posts = Post.objects.filter(user=request.user).order_by('created_at')
    context = {
        'posts': posts,
    }
    return render(request, 'vendor/manage_post.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_post(request):
    if get_vendor(request).is_approved == False:
        messages.success(request,'Sorry, your restaurant has not been licensed')
        return redirect('manage_post')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post_title = form.cleaned_data['post_title']
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            post.slug = slugify(post_title) + '-' + str(post.id)
            post.save()
            messages.success(request,'Post added successfully')
            return redirect('manage_post')
        else:
            print(form.errors)
    else:
        form = PostForm()
    context = {
        'form':form,
    }
    return render(request,'vendor/add_post.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_post(request, pk=None):
    if get_vendor(request).is_approved == False:
        messages.success(request,'Sorry, your restaurant has not been licensed')
        return redirect('manage_post')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post_title = form.cleaned_data['post_title']
            post = form.save(commit=False)
            post.user = request.user
            post.slug = slugify(post_title) + '-' + str(post.id)
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('manage_post')
        else:
            print(form.errors)

    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
        'post':post
    }
    return render(request, 'vendor/edit_post.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_post(request, pk=None):
    if get_vendor(request).is_approved == False:
        messages.success(request,'Sorry, your restaurant has not been licensed')
        return redirect('manage_post')
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.success(request, 'Post has been deleted successfully!')
    return redirect('manage_post')