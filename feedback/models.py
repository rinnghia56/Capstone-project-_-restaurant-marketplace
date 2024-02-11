from django.db import models
from menu.models import FoodItem
from accounts.models import User

# Create your models here.
class Comment(models.Model):
    SENTIMENT = (
        ('Positive', 'Positive'),
        ('Neutral', 'Neutral'),
        ('Negative', 'Negative'),
    )
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=15, choices=SENTIMENT, default='Neutral')

    def __str__(self):
        return f"Comment by {self.user} on {self.food_item}"
    
class Rating(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    value = models.IntegerField(choices=[(i, str(i)) for i in range(1, 5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.value)