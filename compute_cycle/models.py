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


def get_eligible_users(search_locations):
    located_users_queryset = User.objects.filter(locations__in=[search_locations])
    print(located_users_queryset.query)
    located_users = located_users_queryset.get()
    return located_users


def populate_sample_data():
    sasb = Location(common_name="SASB")
    sasb.save()
    meeting = Meeting(proposed_date=timezone.now(), fulfilled_date=timezone.now(), location=sasb.id)


