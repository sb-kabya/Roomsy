from rest_framework import generics, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import Hotel, HotelPhoto, Room
from .serializers import (
    HotelListSerializer, HotelDetailSerializer, HotelWriteSerializer,
    HotelPhotoSerializer, RoomSerializer, RoomWriteSerializer,
)
class HotelListView(generics.ListAPIView):
    """List all hotels. Search: ?search=name/city  Filter: ?city=Dhaka  ?star_rating=5"""
    serializer_class= HotelListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends= [filters.SearchFilter, filters.OrderingFilter]
    search_fields= ['name', 'city', 'country', 'description']
    ordering_fields = ['name','star_rating', 'created_at']

    def get_queryset(self):
        qs = Hotel.objects.filter(is_active=True).prefetch_related('photos', 'reviews', 'rooms')
        city = self.request.query_params.get('city')
        star_rating = self.request.query_params.get('star_rating')
        if city:
            qs = qs.filter(city__icontains=city)
        if star_rating:
            qs = qs.filter(star_rating=star_rating)
        return qs
class HotelDetailView(APIView):
    """Full hotel detail with rooms, photos and reviews."""
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        hotel = get_object_or_404(Hotel, pk=pk, is_active=True)
        serializer = HotelDetailSerializer(hotel, context={'request': request})
        data = serializer.data
        from apps.reviews.serializers import ReviewSerializer
        reviews = hotel.reviews.select_related('user').order_by('-created_at')
        data['reviews'] = ReviewSerializer(reviews, many=True).data
        return Response(data)
class HotelCreateView(generics.CreateAPIView):
    serializer_class = HotelWriteSerializer
    permission_classes = [permissions.IsAdminUser]
class HotelManageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= HotelWriteSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset= Hotel.objects.all()

class HotelPhotoUploadView(APIView):
    permission_classes = [permissions.IsAdminUser]
    parser_classes= [MultiPartParser, FormParser]
    def post(self, request, hotel_id):
        hotel = get_object_or_404(Hotel, pk=hotel_id)
        serializer = HotelPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hotel=hotel)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RoomListView(generics.ListAPIView):
    serializer_class   = RoomSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Room.objects.filter(hotel_id=self.kwargs['hotel_id'])
        if self.request.query_params.get('available'):
            qs = qs.filter(is_available=True)
        return qs
class RoomCreateView(generics.CreateAPIView):
    serializer_class = RoomWriteSerializer
    permission_classes = [permissions.IsAdminUser]
class RoomManageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= RoomWriteSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Room.objects.all()
