from django.urls import path
from . import views
urlpatterns = [
    path('',views.HotelListView.as_view(),name='hotel-list'),
    path('<int:pk>/',views.HotelDetailView.as_view(),name='hotel-detail'),
    path('create/',views.HotelCreateView.as_view(),name='hotel-create'),
    path('<int:pk>/manage/',views.HotelManageView.as_view(),name='hotel-manage'),
    path('<int:hotel_id>/photos/', views.HotelPhotoUploadView.as_view(), name='hotel-photos'),
    path('<int:hotel_id>/rooms/', views.RoomListView.as_view(),name='room-list'),
    path('rooms/create/',views.RoomCreateView.as_view(),name='room-create'),
    path('rooms/<int:pk>/manage/',views.RoomManageView.as_view(),name='room-manage'),
]
