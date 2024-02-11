"""
URL configuration for restaurant_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as MarketplaceViews

urlpatterns = [
    # Jet Admin
    path('jet/', include('jet.urls','jet')),
    path('jet/dashboard/',include('jet.dashboard.urls','jet-dashboard')),
    # Admin
    path('admin/', admin.site.urls),
    # Home
    path('',views.index,name="home"),
    # Account
    path('accounts/',include('accounts.urls')),
    # Marketplace
    path('marketplace/',include('marketplace.urls')),
    # Search
    path('search/', MarketplaceViews.search_food, name='search_food'),
    path('search_address/', MarketplaceViews.search_address, name='search_address'),
    path('search_both/', MarketplaceViews.search_both, name='search_both'),
    path('search_your_location/', MarketplaceViews.search_location, name='search_your_location'),
    # Cart
    path('cart/', MarketplaceViews.cart, name='cart'),
    # Checkout
    path('checkout/',MarketplaceViews.checkout, name="checkout"),
    # Order
    path('orders/',include('orders.urls')),
    # Feedback
    path('feedback/', include('feedback.urls')),
    # About
    path('about/', views.about , name="about"),
    # Blog
    path('blogs/', include('blogs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
