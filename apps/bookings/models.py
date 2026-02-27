import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.hotels.models import Room

User = get_user_model()
class Booking(models.Model):
    STATUS = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    booking_id     = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room           = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date  = models.DateField()
    check_out_date = models.DateField()
    total_nights   = models.IntegerField(default=1)
    total_price    = models.DecimalField(max_digits=10, decimal_places=2)
    status         = models.CharField(max_length=20, choices=STATUS, default='confirmed')
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.email} at {self.room.hotel.name}"

    @property
    def hotel_name(self):
        return self.room.hotel.name
