from django.contrib import admin
from .models import Vendor, OpeningHour


# display on admin
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user','vendor_name','is_approved','create_at')
    list_display_links = ('user','vendor_name')
    list_editable = ('is_approved',)
    search_fields = ('vendor_name',)
    list_filter = ('is_approved',)

class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor','day','from_hour','to_hour')

# Register your models here.
admin.site.register(Vendor,VendorAdmin)
admin.site.register(OpeningHour,OpeningHourAdmin)