from rest_framework import serializers
from .models import Hotel, HotelPhoto, Room
class HotelPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = HotelPhoto
        fields = ['id', 'image', 'caption', 'is_primary']
class RoomSerializer(serializers.ModelSerializer):
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)

    class Meta:
        model  = Room
        fields = ['id', 'room_number', 'room_type', 'room_type_display',
                  'price_per_night', 'capacity', 'is_available']

class RoomWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Room
        fields = ['id', 'hotel', 'room_number', 'room_type',
                  'price_per_night', 'capacity', 'is_available']

class HotelListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    primary_photo = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'city', 'country', 'address', 'star_rating',
                  'amenities', 'average_rating', 'total_reviews', 'primary_photo', 'min_price']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return 0.0
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)

    def get_total_reviews(self, obj):
        return obj.reviews.count()
    def get_min_price(self, obj):
        rooms = obj.rooms.filter(is_available=True)
        if rooms.exists():
            return float(rooms.order_by('price_per_night').first().price_per_night)
        return None

    def get_primary_photo(self, obj):
        photo = obj.photos.filter(is_primary=True).first() or obj.photos.first()
        if photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(photo.image.url)
        return None

class HotelDetailSerializer(serializers.ModelSerializer):
    photos         = HotelPhotoSerializer(many=True, read_only=True)
    rooms          = RoomSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews  = serializers.SerializerMethodField()

    class Meta:
        model  = Hotel
        fields = ['id', 'name', 'description', 'address', 'city', 'country',
                  'star_rating', 'amenities', 'is_active', 'created_at',
                  'average_rating', 'total_reviews', 'photos', 'rooms']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return 0.0
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)

    def get_total_reviews(self, obj):
        return obj.reviews.count()

class HotelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Hotel
        fields = ['id', 'name', 'description', 'address', 'city', 'country',
                  'star_rating', 'amenities', 'is_active']
