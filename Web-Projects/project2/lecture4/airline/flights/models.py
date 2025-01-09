from django.db import models

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    # origin = models.CharField(max_length=64)
    # destination = models.CharField(max_length=64)
    # duration = models.IntegerField()

    # Now, to references another table(which is Airport)
    # From a Flight, I can say flights = Flight.objects.all() !! and say !! flight = flights.first()  after then flight.origin will give me 'New York'
    # For example, if I have an Airport, I can use lhr.arrivals.all() will show every flights arriving London(LHR). lhr는 아래를 보면 알듯이 Airport() object이기 때문에 arrivals라는 related_name으로 destination을 부를수있음
    # 참고로, related_name으로만 Airport object에서만 부를수 있음.(lhr.destination 이런식으론 안됨, 반대로 flight.arrivals 도 안됨 flight.destination만 가능)


    # jfk = Airport(code="JFK", city="New York"), lhr = Airport(code="LHR", city="London")
    # f = Flight(origin=jfk, destination=lhr, duration=415)
    # just typing 'f' --> <Flight: 1: New York (JFK) to London (LHR)> This is because look the Airport __str__
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"


class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)

    # blank=True to allow the possibility that a passenger has no flight. Maybe if they're not registered for any flights at all.
    # ManyToManyField 는 하나의 Flight 오브젝트만을 정할수 있는게 아닌 여러개를 정할수 있게 해준다.
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"