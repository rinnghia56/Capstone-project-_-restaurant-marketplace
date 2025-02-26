from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
import datetime

# form
from .forms import UserForm
from vendor.forms import VendorForm

# model
from .models import User, UserProfile
from vendor.models import Vendor
from orders.models import Order 

# utils 
from .utils import detectUser, send_verification_email 



# Check permission vendor
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    

# Check permission customer
def check_role_cutomer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

# Resgister user
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!')
        return redirect('myAccount')
    if request.method == 'POST':
       form = UserForm(request.POST)
       if form.is_valid():
          first_name = form.cleaned_data['first_name']
          last_name = form.cleaned_data['last_name']
          username = form.cleaned_data['username']
          email = form.cleaned_data['email']
          password = form.cleaned_data['password']
          user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,password=password,email=email)
          user.role = User.CUSTOMER
          user.save()

          # Send verification email
          mail_subject = 'Please activate your account'
          email_template = 'accounts/emails/account_verification_email.html'
          send_verification_email(request,user,mail_subject,email_template)
          messages.success(request, 'Your account has been registered successfully!')
          return redirect(registerUser)
       else:
           print(form.errors)
    else:
        form = UserForm()
    
    return render(request,'accounts/registerUser.html',{'form':form})

# Register Vendor
def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
              first_name = form.cleaned_data['first_name']
              last_name = form.cleaned_data['last_name']
              username = form.cleaned_data['username']
              email = form.cleaned_data['email']
              password = form.cleaned_data['password']
              user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,password=password,email=email)
              user.role = User.VENDOR
              user.save()
              vendor = v_form.save(commit=False)
              vendor.user = user
              vendor_name = v_form.cleaned_data['vendor_name']
              vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
              user_profile = UserProfile.objects.get(user=user)
              vendor.user_profile = user_profile

              
              # Send verification email
              mail_subject = 'Please activate your account'
              email_template = 'accounts/emails/account_verification_email.html'
              send_verification_email(request,user,mail_subject,email_template)
              vendor.save()
              messages.success(request,'Your account has been registered successfully! Please wait for the approval')
              return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form':form,
        'v_form':v_form
    }
    return render(request,'accounts/registerVendor.html',context)

# Login
def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

# Logout
def logout(request):
    auth.logout(request)
    messages.info(request,'You are now logged out')
    return redirect('login')

# My Account
@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

# Customer
@login_required(login_url='login')
@user_passes_test(check_role_cutomer)
def cusDashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_profile = UserProfile.objects.get(user=request.user)
    total_money = 0
    if len(orders) > 0:
        total_money = sum(order.total for order in orders)

    current_month = timezone.now().month
    current_year = timezone.now().year
    orders_current_month = Order.objects.filter(Q(user=request.user) &
    Q(created_at__month=current_month) & Q(created_at__year=current_year) & Q(is_ordered=True))

    total_money_current = 0
    if len(orders_current_month) > 0:
        total_money_current = sum(order.total for order in orders_current_month)

    context = {
        'orders':orders,
        'order_count':orders.count(),
        'user_profile':user_profile,
        'total_money':total_money,
        'total_money_current':total_money_current,
        'page_obj':page_obj

    }
    return render (request,'accounts/cusDashboard.html', context)

# Vendor Dashboard
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def venDashboard(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at')
    recent_orders = orders[:8]

    # current month's revenue
    current_month = datetime.datetime.now().month
    current_month_orders = orders.filter(vendors__in=[vendor.id], created_at__month=current_month)
    current_month_revenue = 0
    for i in current_month_orders:
        current_month_revenue += i.get_total_by_vendor()['grand_total']


    # total revenue
    total_revenue = 0
    for i in orders:
        total_revenue += i.get_total_by_vendor()['grand_total']


    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
        'total_revenue':total_revenue,
        'current_month_revenue':current_month_revenue
    }
    return render (request,'accounts/venDashboard.html',context)

# Activate Account
def activate(request,uidb64,token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('myAccount')
    

# Forgot password
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request, 'Password reset link has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request,'Acccount does not exist')
            return redirect('forgot_password')
    return render(request,"accounts/forgot_password.html")

# Reset password validate
def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('myAccount')

# Reset password
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not exits')
            return redirect('reset_password')
    return render(request,"accounts/reset_password.html")

# Forgot password customer
def forgot_password_customer(request):
    auth.logout(request)
    messages.info(request,'You are now logged out')
    return redirect('forgot_password')