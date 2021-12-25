from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = ("categories")


class Listing(models.Model):
    title = models.CharField(max_length=64)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    discription = models.TextField()
    image = models.URLField()
    price = models.DecimalField("Starting Bid", max_digits=6, decimal_places=2)
    category = ForeignKey(Category, on_delete=models.CASCADE, related_name="cat_listings")
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    best_bidder = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="best_bidder")

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-date']


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} 💬 {self.listing.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} 💵 {self.listing.title}"
