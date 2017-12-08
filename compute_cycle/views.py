from django.shortcuts import render

from django.http import HttpResponse

from .models import Location
from .models import get_eligible_users, populate_sample_data


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

