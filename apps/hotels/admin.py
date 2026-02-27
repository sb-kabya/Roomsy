from django.contrib import admin
from .models import Hotel, HotelPhoto, Room
class HotelPhotoInline(admin.TabularInline):
    model  = HotelPhoto
    extra  = 1
    fields = ['image', 'caption', 'is_primary']
class RoomInline(admin.TabularInline):
    model  = Room
    extra  = 1
    fields = ['room_number', 'room_type', 'price_per_night', 'capacity', 'is_available']

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display  = ['name', 'city', 'country', 'star_rating', 'is_active', 'created_at']
    list_filter   = ['star_rating', 'is_active', 'country']
    search_fields = ['name', 'city', 'country']
    list_editable = ['is_active']
    inlines       = [HotelPhotoInline, RoomInline]

@admin.register(HotelPhoto)
class HotelPhotoAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'caption', 'is_primary']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display  = ['hotel', 'room_number', 'room_type', 'price_per_night', 'capacity', 'is_available']
    list_filter   = ['hotel', 'room_type', 'is_available']
    search_fields = ['hotel__name', 'room_number']
    list_editable = ['is_available', 'price_per_night']
