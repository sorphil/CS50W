from django.shortcuts import render
from .models import *
from django.urls import reverse
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
    return render (request, "flights/index.html", {'flights': Flight.objects.all()})

def flight(request, id):
    
    flight = Flight.objects.get(pk = id)
    nonpassengers = Passenger.objects.filter(flights=None)
    passengers = flight.passengers.all()
    print(nonpassengers)
    return render (request, "flights/flight.html", {
        'flight': flight,
        "passengers": passengers,
        "nonpassengers":nonpassengers
        })


def book(request, id):
    if request.method == "POST":
        flight = Flight.objects.get(pk = id)
        passenger = Passenger.objects.get(pk = int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse('flight', args = (flight.id,)))
    if request.method == "GET":
        return render(request, "f")