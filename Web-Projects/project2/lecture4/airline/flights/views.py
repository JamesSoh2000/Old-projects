from django.shortcuts import render, redirect
from .models import Flight, Passenger
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    # pk is referencing primary key, but known as id here.
    flight = Flight.objects.get(pk=flight_id)

    # If I want a dropdown where I can choose from all the people who aren't already on the flight, to register one of them.
    # The function in non-passenger excluding the passengers who are already on the flight
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })


def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        # When someone submits this form to book a new passenger on the flight,
        # They should tell me what the ID is of the passenger. What passenger should I book on the flight?
        # I need the flight and the passenger information to book a flight.
        # request.GET은 GET으로 받는 인자들을 다 포함하는 딕셔너리 객체이다.(POST도 똑같음)
        # request.POST['passenger'] whatever was submitted via this post form named 'passenger'
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))