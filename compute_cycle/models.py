import datetime

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
        if self.fulfilled_date:
            timestamp = self.fulfilled_date.strftime('%b %d, %Y at %H:%M')
        else:
            timestamp = None
        description = "Meeting: %s" % (timestamp)
        return description


    def is_recent(self):
        return self.fulfilled_date >= timezone.now() - datetime.timedelta(days=30)


# search_location_ids should be a lis of integer primary key ids of the Location table
def get_eligible_users(search_location_ids):
    located_users_queryset = User.objects.filter(locations__in=search_location_ids)
    #print(located_users_queryset.query)
    located_users = located_users_queryset.all()
    #print("\n\n\n")
    #print(located_users)
    return located_users


# person is a user object
# given this person, find out the locations they're willing to meet.
# for those locations, find all users who do not already have meetings scheduled.
# winnow those users down to those who have not met this person recently.
# out of that list, select a random user, and return that user
def find_user_match(person):
    # TODO: checking in case don't find locations
    eligible_locations = person.locations.all()

    # find people in locations person signed up for
    eligible_users = get_eligible_users(eligible_locations)

    # for each candidate, find all meetings these two people have had, sorted by date
    for candidate in eligible_users:
        # TODO: returns duplicate meetings, fix
        # Note: the minus makes it a desc order
        meetings = Meeting.objects.filter(attendees__in=[person, candidate]).order_by('-fulfilled_date').all()
        if (meetings and meetings.count() > 0):
            # if the most recent meeting is not recent enough, match these users
            if (not meetings[0].is_recent()):
                # create a new meeting, and return the two users and the new meeting
                tomorrow = timezone.now() + datetime.timedelta(days=1)
                # TODO: currently not checking whether the proposed location is acceptable to both people
                new_meeting_1, created = Meeting.objects.get_or_create(proposed_date=timezone.now(), fulfilled_date=tomorrow, location=eligible_locations[0])
                # TODO: change to only add person if not already in the ManyToMany users field
                if (created):
                    new_meeting_1.attendees.add(person)
                    new_meeting_1.attendees.add(candidate)
                    new_meeting_1.save()

                    # TODO:  yeah, error and logic and assumption handling
                    return (person, candidate, new_meeting_1)
    return ()



def populate_sample_data():
    #person_admin, created = User.objects.get_or_create(name="Admin", email="admin@nypl.org", is_admin=True)

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

    week_ago = timezone.now() - datetime.timedelta(days=7)
    two_months_ago = timezone.now() - datetime.timedelta(days=60)

    sasb_meeting_1, created = Meeting.objects.get_or_create(proposed_date=timezone.now(), fulfilled_date=week_ago, location=sasb)
    # TODO: change to only add person if not already in the ManyToMany users field
    if (created):
        sasb_meeting_1.attendees.add(person1)
        sasb_meeting_1.attendees.add(person2)
        sasb_meeting_1.save()

    sasb_meeting_2, created = Meeting.objects.get_or_create(proposed_date=timezone.now(), fulfilled_date=two_months_ago, location=sasb)
    if (created):
        sasb_meeting_2.attendees.add(person1)
        sasb_meeting_2.attendees.add(person3)
        sasb_meeting_2.save()

    lsc_meeting_1, created = Meeting.objects.get_or_create(proposed_date=timezone.now(), fulfilled_date=two_months_ago, location=lsc)
    if (created):
        lsc_meeting_1.attendees.add(person2)
        lsc_meeting_1.attendees.add(person3)
        lsc_meeting_1.save()


