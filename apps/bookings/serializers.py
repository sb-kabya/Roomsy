from rest_framework import serializers
from django.utils import timezone
from .models import Booking
from apps.hotels.serializers import RoomSerializer
class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Booking
        fields = ['room', 'check_in_date', 'check_out_date']

    def validate(self, attrs):
        check_in  = attrs['check_in_date']
        check_out = attrs['check_out_date']
        room      = attrs['room']

        if check_in < timezone.now().date():
            raise serializers.ValidationError('Check-in date cannot be in the past.')
        if check_in >= check_out:
            raise serializers.ValidationError('Check-out must be after check-in.')
        if not room.is_available:
            raise serializers.ValidationError('This room is not available.')
        overlap = Booking.objects.filter(
            room=room,
            status='confirmed',
            check_in_date__lt=check_out,
            check_out_date__gt=check_in,
        )
        if overlap.exists():
            raise serializers.ValidationError('Room is already booked for these dates.')
        return attrs

class BookingSerializer(serializers.ModelSerializer):
    room_info  = RoomSerializer(source='room', read_only=True)
    hotel_name = serializers.ReadOnlyField()
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model  = Booking
        fields = ['id', 'booking_id', 'user_email', 'room_info', 'hotel_name',
                  'check_in_date', 'check_out_date', 'total_nights',
                  'total_price', 'status', 'created_at']
