from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_name  = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.CharField(source='user.email',read_only=True)
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    class Meta:
        model  = Review
        fields = ['id', 'hotel', 'hotel_name', 'user_name', 'user_email',
                  'rating', 'comment', 'created_at', 'updated_at']

class ReviewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = ['hotel', 'rating', 'comment']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value
