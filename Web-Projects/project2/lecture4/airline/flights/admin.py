from django.contrib import admin
from .models import Flight, Airport, Passenger

# This is subclass of model admin(admin page) 이건 전부 admin 페이지에 기능을 추가하는거임
# I can specify any particular setting that I want to apply to
# how the flight admin page is displayed
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")

# 이거는 그냥 Chosen flights라는 칸을 하나 더 만들어서 Available flights에서 더블클릭해서 그걸 옮길수있음.
class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)
# Register your models here.
admin.site.register(Airport)
# When you register the Flight, use the FlightAdmin settings when you do so.
# Then when you go to flight page(admin/flights/flight), now u see id, origin, destination, and duration.(it didn't show id before)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)