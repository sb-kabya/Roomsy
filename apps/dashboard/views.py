from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
from django.db.models import Count, Sum, Q
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from apps.bookings.models import Booking
from apps.hotels.models import Hotel, Room
from apps.reviews.models import Review
User = get_user_model()
CONFIRMED = ['confirmed', 'completed']
class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        today = timezone.now().date()
        this_month_start = today.replace(day=1)
        confirmed = Booking.objects.filter(status__in=CONFIRMED)
        total_bookings = confirmed.count()
        cancelled_bookings = Booking.objects.filter(status='cancelled').count()
        total_revenue = confirmed.aggregate(
            total=Sum('total_price')
        )['total'] or 0
        this_month_revenue = confirmed.filter(
            created_at__date__gte=this_month_start
        ).aggregate(
            total=Sum('total_price')
        )['total'] or 0
        return Response({
            "booking_statistics": {
                "total_bookings": total_bookings,
                "cancelled_bookings": cancelled_bookings,
            },
            "revenue_statistics": {
                "total_revenue": float(total_revenue),
                "this_month_revenue": float(this_month_revenue),
            },
            "user_statistics": {
                "total_users": User.objects.count(),
            },
            "room_statistics": {
                "total_rooms": Room.objects.count(),
                "available_rooms": Room.objects.filter(is_available=True).count(),
            },
        })
class BookingTrendsView(APIView):    
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        days  = min(int(request.query_params.get('days', 30)), 365)
        start = timezone.now().date()- timedelta(days=days)
        trend = list(
            Booking.objects.filter(created_at__date__gte=start, status__in=CONFIRMED)
            .values('created_at__date')
            .annotate(bookings=Count('id'), revenue=Sum('total_price'))
            .order_by('created_at__date')
        )
        return Response({
            'days': days,
            'trend': [
                {'date': str(t['created_at__date']), 'bookings': t['bookings'], 'revenue': float(t['revenue'] or 0)}
                for t in trend
            ],
        })
def root_view(request):
    return JsonResponse({"message": "Roomsy API is running!"})