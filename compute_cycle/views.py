from django.shortcuts import render

from django.http import HttpResponse

from .models import Location, User
from .models import find_user_match, get_eligible_users, populate_sample_data


def index(request):
    return HttpResponse("computing urls")


def prepopulate(request):
    populate_sample_data()
    return HttpResponse("populated")


def sasb_users(request):
    search_locations = Location.objects.filter(common_name="SASB")
    location_ids = []
    for location in search_locations:
        location_ids.append(location.id)

    users = get_eligible_users(location_ids)
    return HttpResponse("users")

def find_coffee_match(request):
    person3, created = User.objects.get_or_create(name="Chancey", email="chancey@nypl.org")
    find_user_match(person3)
    return HttpResponse("You Will Coffeeeeeeee")
