from django.urls import path
from . import views

urlpatterns = [
    path('hotel/<int:hotel_id>/', views.HotelReviewListView.as_view(), name='hotel-reviews'),
    path('create/', views.ReviewCreateView.as_view(),name='review-create'),
    path('<int:pk>/', views.ReviewDetailView.as_view(),name='review-detail'),
    path('my/', views.MyReviewsView.as_view(), name='my-reviews'),
]
