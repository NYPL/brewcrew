from django.db import models
from django.utils import timezone

from accounts.models import Location, User


class Meeting(models.Model):
    proposed_date = models.DateTimeField('proposed date')
    # optional first positional argument to a Field to designate a human-readable name
    fulfilled_date = models.DateTimeField('date meeting occurred')

    # TODO: we might want to DO_NOTHING or SET(callable) instead of CASCADE
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    attendees = models.ManyToManyField(User)

    #spring_constant = models.CharField(max_length=200)
    #spring_constant = models.IntegerField(default=0)

    def __str__(self):
        return self.fulfilled_date


    def is_recent(self):
        return self.fulfilled_date >= timezone.now() - datetime.timedelta(days=30)


def get_eligible_users(search_location_ids):
    located_users_queryset = User.objects.filter(locations__in=search_location_ids)
    print(located_users_queryset.query)
    located_users = located_users_queryset.all()
    print("\n\n\n")
    print(located_users)
    return located_users


def populate_sample_data():
    sasb, created = Location.objects.get_or_create(common_name="SASB")
    if (created):
        sasb.save()
    lsc, created = Location.objects.get_or_create(common_name="LSC")
    if (created):
        lsc.save()

    person1, created = User.objects.get_or_create(name="Alice", email="alice@nypl.org")
    # TODO: change to only add location if not already in the ManyToMany locations field
    if (created):
        person1.locations.add(sasb)
        person1.save()

    person2, created = User.objects.get_or_create(name="Bob", email="bob@nypl.org")
    if (created):
        person2.locations.add(sasb)
        person2.locations.add(lsc)
        person2.save()

    person3, created = User.objects.get_or_create(name="Chancey", email="chancey@nypl.org")
    if (created):
        person3.locations.add(sasb)
        person3.locations.add(lsc)
        person3.save()

    sasb_meeting_1, created = Meeting.objects.get_or_create(proposed_date=timezone.now(), fulfilled_date=timezone.now(), location=sasb)
    # TODO: change to only add person if not already in the ManyToMany users field
    if (created):
        sasb_meeting_1.attendees.add(person1)
        sasb_meeting_1.attendees.add(person2)
        sasb_meeting_1.save()

    sasb_meeting_2, created = Meeting.objects.get_or_create(proposed_date=timezone.now(), fulfilled_date=timezone.now(), location=sasb)
    if (created):
        sasb_meeting_2.attendees.add(person1)
        sasb_meeting_2.attendees.add(person3)
        sasb_meeting_2.save()

    lsc_meeting_1, created = Meeting.objects.get_or_create(proposed_date=timezone.now(), fulfilled_date=timezone.now(), location=lsc)
    if (created):
        lsc_meeting_1.attendees.add(person2)
        lsc_meeting_1.attendees.add(person3)
        lsc_meeting_1.save()


