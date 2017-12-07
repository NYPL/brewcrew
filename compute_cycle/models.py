from django.db import models

#class Node(models.Model):
#    question_text = models.CharField(max_length=200)
#
#    # optional first positional argument to a Field to designate a human-readable name
#    pub_date = models.DateTimeField('date published')


class Edge(models.Model):
    #start_node = models.ForeignKey(Question, on_delete=models.CASCADE)
    #end_node = models.ForeignKey(Question, on_delete=models.CASCADE)
    #spring_constant = models.CharField(max_length=200)
    spring_constant = models.IntegerField(default=0)

