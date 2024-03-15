from django.db import models
from area.models import Area
from django.db.models import Avg,Count
from django.contrib.auth.models import User
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='photos/hotels')
    address = models.CharField(max_length=255)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)  # Update field name
    country = models.CharField(max_length=100)
    total_rooms = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def averageReview(self):
        reviews = Review.objects.filter(hotel=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    def countReview(self):
        reviews = Review.objects.filter(hotel=self,status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

class Room(models.Model):
    DELUXE = 'Deluxe'
    SINGLE = 'Single'
    DOUBLE = 'Double'
    ROOM_CATEGORIES = [
        (DELUXE, 'Deluxe'),
        (SINGLE, 'Single'),
        (DOUBLE, 'Double'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=10, choices=ROOM_CATEGORIES, default='Double')
    bed_count = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.name} - Room {self.room_type}"

class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject