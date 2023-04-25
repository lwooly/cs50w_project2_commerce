from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction_listing(models.Model):
    listing_title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    bid = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=200)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller") 

    def __str__(self):
        return f"Listing {self.id}: {self.name} {self.bid}"