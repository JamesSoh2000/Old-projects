from django.contrib import admin

# Register your models here.
# 여기 admin 들어갈때 아이디 justlikethat17  비번 hl3ewr14
from .models import User, Listing, Bid, Comment, Category, WatchList

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(WatchList)