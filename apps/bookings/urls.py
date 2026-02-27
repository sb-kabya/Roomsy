from django.urls import path
from . import views

urlpatterns = [
    path('',views.MyBookingsView.as_view(),name='my-bookings'),
    path('create/',views.BookingCreateView.as_view(), name='booking-create'),
    path('<int:pk>/',views.BookingDetailView.as_view(), name='booking-detail'),
    path('<uuid:booking_id>/cancel/', views.CancelBookingView.as_view(), name='booking-cancel'),
    path('all/',views.AllBookingsView.as_view(), name='all-bookings'),
]
