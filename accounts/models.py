from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'Faculty'),
        (3, 'Student'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3) # Default to student

    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"

# --- NEW MODEL ---
class RegistrationRequest(models.Model):
    """
    Stores data for users who have registered but are pending admin approval.
    """
    USER_TYPE_CHOICES = (
        (2, 'Faculty'),
        (3, 'Student'),
    )
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) # Stores hashed password
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.username} ({self.get_user_type_display()})"