from django.contrib import admin
from .models import Category, FoodItem , CategoryDefault, FoodImage, FoodFavorite


    
class CategoryDefaultAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','created_at')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','vendor','updated_at',)
    search_fields = ('category_name','vendor__vendor_name',)

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('food_title',)}
    list_display = ('food_title','category','vendor','price','is_available','updated_at')
    search_fields = ('food_title','category__category_name','vendor__vendor_name','price')
    list_filter = ('is_available',)

class FoodImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'food_item','image')
    list_filter = ('food_item',)
    search_fields = ('food_item__food_title',)

class FoodFavoriteAdmin(admin.ModelAdmin):
    list_display = ('id','user','food_item')



admin.site.register(CategoryDefault, CategoryDefaultAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(FoodItem,FoodItemAdmin)
admin.site.register(FoodImage, FoodImageAdmin)
admin.site.register(FoodFavorite, FoodFavoriteAdmin)
