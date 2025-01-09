# . means it's the same directory. And import views.py(which is in same directory as urls.py.)
from django.urls import path
from . import views

# List of all of the URLs that can be accessed for this particular app.

# "" means nothing after end of the route.
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.greet, name="greet")
]

