from django.contrib import admin

# Register your models here.

from .models import User, Listing, Bid, Category, Comment, WatchList

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(WatchList)