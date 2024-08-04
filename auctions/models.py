from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", related_name="watchlisteners")

class Listing(models.Model):
    title = models.CharField(max_length=255)
    descripcion = models.TextField()
    starting_bid = models.FloatField()
    image = models.TextField()
    created_at = models.DateTimeField(default=timezone.now())
    open = models.BooleanField(default=True)
    creator = models.ForeignKey("User", on_delete=models.CASCADE, related_name="listings")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="listings")
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="won_auctions")
    def max_bid(self):
        return self.bids.order_by('-amount').first()
    def __str__(self):
        return self.title

class Bid(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField()

class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now())

class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
