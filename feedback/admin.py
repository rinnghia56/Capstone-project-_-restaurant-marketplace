from django.contrib import admin
from .models import Comment, Rating

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ('food_item','user','created_at')
    search_fields = ('user__username',)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('food_item','user','created_at','value')
    search_fields = ('user__username',)


admin.site.register(Comment,CommentAdmin)
admin.site.register(Rating,RatingAdmin)