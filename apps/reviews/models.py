from django.db import models
from django.contrib.auth import get_user_model
from apps.hotels.models import Hotel

User = get_user_model()
class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['hotel', 'user']
    def __str__(self):
        return f"{self.user.email} - {self.hotel.name} - {self.rating}/5"
