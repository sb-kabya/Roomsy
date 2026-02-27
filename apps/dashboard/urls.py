from django.urls import path
from . import views

urlpatterns = [
    path('',views.AdminDashboardView.as_view(), name='dashboard'),
    path('trends/', views.BookingTrendsView.as_view(),  name='trends'),
]
