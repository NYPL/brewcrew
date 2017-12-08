from django.db import models
from django.utils import timezone


class Location(models.Model):
    common_name = models.CharField(max_length=200)

    def __str__(self):
        return self.common_name

        class Meta:
            ordering = ('common_name', )


class Person(models.Model):
    locations = models.ManyToManyField(Location)
#    question_text = models.CharField(max_length=200)
#
#    # optional first positional argument to a Field to designate a human-readable name
#    def was_published_recently(self):
#        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        #TODO: concatenate name and locations
        return self.locations


class Meeting(models.Model):
    proposed_date = models.DateTimeField('proposed date')
    fulfilled_date = models.DateTimeField('date meeting occurred')

    # TODO: we might want to DO_NOTHING or SET(callable) instead of CASCADE
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    #end_node = models.ForeignKey(Question, on_delete=models.CASCADE)
    #spring_constant = models.CharField(max_length=200)
    #spring_constant = models.IntegerField(default=0)

    def __str__(self):
        return self.fulfilled_date


def get_eligible_users():
    


