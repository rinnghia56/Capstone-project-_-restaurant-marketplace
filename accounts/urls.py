from django.urls import path, include
from . import views


urlpatterns = [
    # permission
    path('',views.myAccount),
    # register
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),

    # login
    path('login/', views.login,name='login'),
    # logout
    path('logout/', views.logout,name='logout'),
    # my account
    path('myAccount/',views.myAccount,name='myAccount'),
    # Dashboard customer
    path('cusdashboard/',views.cusDashboard,name='cusDashboard'),
    # Dashboard vendor
    path('vendashboard/',views.venDashboard,name='venDashboard'),

    # activate account
    path('activate/<uidb64>/<token>',views.activate,name='activate'),

    # password
    path('forgot_password/', views.forgot_password,name='forgot_password'),
    path('forgot_password_customer/', views.forgot_password_customer,name='forgot_password_customer'),
    path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate,name='reset_password_validate'),
    path('reset_password/', views.reset_password,name='reset_password'),

    # vendor
    path('vendor/', include('vendor.urls')),

    #account
    path('customer/', include('customers.urls')),
]