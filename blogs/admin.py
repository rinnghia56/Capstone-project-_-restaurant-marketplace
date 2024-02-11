from django.contrib import admin
from .models import CategoryBlog, Post
# Register your models here.


class CategoryDefaultAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','created_at')
    search_fields = ('category_name',)

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('post_title',)}
    list_display = ('post_title','user','created_at',)
    search_fields = ('post_title',)



admin.site.register(CategoryBlog,CategoryDefaultAdmin)
admin.site.register(Post,PostAdmin)
