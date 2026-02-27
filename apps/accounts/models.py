from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email             = models.EmailField(unique=True)
    balance           = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    phone_number      = models.CharField(max_length=20, blank=True)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
