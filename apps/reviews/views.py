from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer, ReviewWriteSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class HotelReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        return Review.objects.filter(hotel_id=self.kwargs['hotel_id']).select_related('user', 'hotel')
class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        hotel = serializer.validated_data['hotel']
        if Review.objects.filter(hotel=hotel, user=self.request.user).exists():
            raise PermissionDenied('You already reviewed this hotel. Edit your existing review.')
        serializer.save(user=self.request.user)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        review = Review.objects.get(
            hotel=serializer.validated_data['hotel'], user=request.user
        )
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Review.objects.all().select_related('user', 'hotel')
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ReviewWriteSerializer
        return ReviewSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {k: v for k, v in request.data.items() if k != 'hotel'}
        serializer = ReviewWriteSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ReviewSerializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response({'message': 'Review deleted.'}, status=status.HTTP_204_NO_CONTENT)
class MyReviewsView(generics.ListAPIView):
    serializer_class   = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related('hotel')
