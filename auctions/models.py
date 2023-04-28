from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Auction_listing", blank=True, related_name="watchers")


class Auction_listing(models.Model):
    listing_title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    image_url = models.URLField(max_length=200)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", null=True)
    closed = models.BooleanField(default=False)
    category = models.CharField(max_length=32)


class Bid(models.Model):
    bid = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="listing_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")

