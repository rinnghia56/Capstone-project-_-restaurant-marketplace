python manage.py collectstatic

# def vendor_details(request, vendor_slug):
#     vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
#     categories = Category.objects.filter(vendor=vendor).prefetch_related(
#         Prefetch(
#             'fooditems',
#             queryset = FoodItem.objects.filter(is_available=True)
#         )
#     )

#     if request.user.is_authenticated():
#         cart_items = Cart.objects.filter(user=request.user)
#     else:
#         cart_items = None

#     context = {
#         'vendor':vendor,
#         'categories':categories,
#         'cart_items': cart_items
#     }
#     return render(request,'marketplace/vendor_detail.html', context)
