from django.contrib import admin
from .models import Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display    = ['short_id', 'user', 'hotel_name', 'check_in_date', 'check_out_date', 'total_price', 'status', 'created_at']
    list_filter     = ['status', 'created_at']
    search_fields   = ['user__email', 'room__hotel__name']
    readonly_fields = ['booking_id', 'total_nights', 'total_price', 'created_at']

    def short_id(self, obj):
        return str(obj.booking_id)[:8].upper()
    short_id.short_description = 'Booking ID'
    def hotel_name(self, obj):
        return obj.room.hotel.name
    hotel_name.short_description = 'Hotel'
