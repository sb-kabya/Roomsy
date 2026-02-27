from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address= models.CharField(max_length=500)
    city= models.CharField(max_length=100)
    country= models.CharField(max_length=100)
    star_rating = models.IntegerField(default=3)
    amenities= models.TextField(blank=True, help_text='e.g. Pool, WiFi, Gym')
    is_active= models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class HotelPhoto(models.Model):
    hotel= models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='photos')
    image= models.ImageField(upload_to='hotels/')
    caption= models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Photo of {self.hotel.name}"
class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite',  'Suite'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number= models.CharField(max_length=10)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity= models.IntegerField(default=2)
    is_available= models.BooleanField(default=True)
    def __str__(self):
        return f"Room {self.room_number} - {self.hotel.name}"
