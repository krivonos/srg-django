from django.db import models
import time
import datetime
import re

# Create your models here.

class Conference(models.Model):
    title = models.CharField(max_length=100)
    key = models.CharField(max_length=10)
    DayNumber = models.IntegerField()
    DateCal = models.DateField(blank=True, null=True)
    read_only = models.BooleanField("Read only",default=False)
    def __unicode__(self):
        return self.name+' '+"%i" % (self.DayNumber)
    def get_absolute_url(self):
        return "/srg/plan/%i/" % (self.DayNumber)

