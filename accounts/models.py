from django.db import models
from django.contrib.auth.models import User
from hotels.models import Room,Hotel
from django.utils import timezone

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Rating out of 5, for example
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.user.username} for {self.hotel.name}"