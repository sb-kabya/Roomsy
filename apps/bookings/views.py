from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer
from .utils import send_booking_confirmation

class BookingCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        room      = serializer.validated_data['room']
        check_in  = serializer.validated_data['check_in_date']
        check_out = serializer.validated_data['check_out_date']
        nights    = (check_out - check_in).days
        price     = room.price_per_night * nights
        user      = request.user

        if user.balance < price:
            return Response({
                'error': f'Insufficient balance. Required: ${price}, Available: ${user.balance}. '
                         f'Please deposit via POST /api/accounts/deposit/'
            }, status=status.HTTP_400_BAD_REQUEST)

        user.balance -= price
        user.save(update_fields=['balance'])

        booking = serializer.save(
            user=user,
            total_nights=nights,
            total_price=price,
            status='confirmed',
        )
        send_booking_confirmation(booking)
        return Response({
            'message':'Booking confirmed! Check your email.',
            'booking':BookingSerializer(booking).data,
            'remaining_balance':float(user.balance),
        }, status=status.HTTP_201_CREATED)

class MyBookingsView(generics.ListAPIView):
    serializer_class   = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
        return Booking.objects.filter(user=self.request.user)
class BookingDetailView(generics.RetrieveAPIView):
    serializer_class   = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
        return Booking.objects.filter(user=self.request.user)

class CancelBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(booking_id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        if booking.status == 'cancelled':
            return Response({'error': 'Already cancelled.'}, status=status.HTTP_400_BAD_REQUEST)

        if booking.check_in_date <= timezone.now().date():
            return Response({'error': 'Cannot cancel after check-in date.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.balance += booking.total_price
        request.user.save(update_fields=['balance'])
        booking.status = 'cancelled'
        booking.save(update_fields=['status'])

        return Response({
            'message':     f'Booking cancelled. ${booking.total_price} refunded.',
            'new_balance': float(request.user.balance),
        })
class AllBookingsView(generics.ListAPIView):
    serializer_class   = BookingSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Booking.objects.all().select_related('room', 'room__hotel', 'user')
