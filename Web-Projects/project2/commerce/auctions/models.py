from django.contrib.auth.models import AbstractUser
from django.db import models

# AbstractUser, it will already have fields for a username, email, password, etc.,
# !!!중요!!!   Django automatically creates an id field as primary key.
class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listing_category")
    categories = models.ManyToManyField(Category, blank=True, related_name="select_category") # all categories to select from
    image_url = models.URLField(default='google.com')
    sold = models.BooleanField(default=False) # To check if the item is sold out or not

    def __str__(self):
        return f"{self.title} posted by {self.user}"

# 경매가
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2) # the price for offering (제시금액)

    def __str__(self):
        return f"bid on item: {self.listing} by {self.user} with price: {self.price}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment} by {self.user}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    watching = models.BooleanField(default=False)