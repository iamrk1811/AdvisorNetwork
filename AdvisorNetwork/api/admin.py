from django.contrib import admin

# Register your models here.
from .models import Advisor, User, Booking
# Register your models here.
class AdvisorAdmin(admin.ModelAdmin):
    list_display = ('id', 'advisor_name', 'advisor_img_url')
    


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(Advisor, AdvisorAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Booking, BookingAdmin)