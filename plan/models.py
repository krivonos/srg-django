import logging
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
import time
import datetime
import re
from django.core.validators import MaxLengthValidator,MinValueValidator,MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _, ugettext_noop as _noop

# Create your models here.

LaunchDate = datetime.date(2019, 4, 12)

class Day(models.Model):
    title = models.CharField(max_length=100)
    Notes = models.TextField("Notes",max_length=2000, null=True, blank=True, validators=[MaxLengthValidator(1600)])
    date = models.DateField(blank=True, null=True)
    DayNumber = models.IntegerField()
    modified = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return 'Day: ' + "%i" % (self.DayNumber)
    def __str__(self):
        return 'Day: ' + "%i" % (self.DayNumber)

class SessionBearLakes(models.Model):
    Day = models.OneToOneField(Day, on_delete=models.CASCADE,verbose_name="Day", related_name="BearLakesDay",null=True)
    title = models.CharField(max_length=100,blank=True)
    TimeBegin = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(24)])
    TimeEnd = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(24)])
    sysSessionRequest = models.IntegerField(default=0)
    eroSessionRequest = models.IntegerField(default=0)
    artSessionRequest = models.IntegerField(default=0)
    sysNotes = models.TextField("System Notes",max_length=2000, null=True, blank=True, validators=[MaxLengthValidator(1600)])
    eroNotes = models.TextField("eRosita Notes",max_length=2000, null=True, blank=True, validators=[MaxLengthValidator(1600)])
    artNotes = models.TextField("ART-XC Notes",max_length=2000, null=True, blank=True, validators=[MaxLengthValidator(1600)])
    def clean(self, *args, **kwargs):
        # add custom validation here
        session_duration_min=(self.TimeEnd-self.TimeBegin)*60
        request_min=(self.sysSessionRequest+self.eroSessionRequest+self.artSessionRequest)
        if (self.TimeBegin >= self.TimeEnd ):
            raise forms.ValidationError("Session begin time (day hour %i/24) cannot be after (or equal to) End time (day hour %i/24)" % (self.TimeBegin,self.TimeEnd))
        if (request_min>session_duration_min):
            msg="Total requested time (sys:%i + ero:%i + art:%i = %i min) cannot be longer than session duration: %i min" % (self.sysSessionRequest,
                                                                                                                            self.eroSessionRequest,
                                                                                                                            self.artSessionRequest,
                                                                                                                            request_min, 
                                                                                                                            session_duration_min)
            raise forms.ValidationError(msg)
        super(SessionBearLakes, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(SessionBearLakes, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.title
    def __str__(self):
        return 'Session: Day '  + "%i" % (self.Day.DayNumber)
    def get_absolute_url(self):
        return "/plan/BearLakes/%i/show" % (self.Day.DayNumber)
    def get_update_url(self):
        return "/plan/BearLakes/%i/update" % (self.Day.DayNumber)

    
class SessionBearLakesForm(forms.ModelForm):
    class Meta:
        model=SessionBearLakes
        fields=('title','TimeBegin','TimeEnd','sysSessionRequest','eroSessionRequest','artSessionRequest','sysNotes','eroNotes','artNotes')
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 620px;', 'class': 'title'}),
            'TimeBegin': forms.TextInput(attrs={'style': 'width: 620px;', 'class': 'title'}),
            'TimeEnd': forms.TextInput(attrs={'style': 'width: 620px;', 'class': 'title'}),
            'sysSessionRequest': forms.TextInput(attrs={'style': 'width: 150px;', 'class': 'title'}),
            'eroSessionRequest': forms.TextInput(attrs={'style': 'width: 150px;', 'class': 'title'}),
            'artSessionRequest': forms.TextInput(attrs={'style': 'width: 150px;', 'class': 'title'}),
            'sysNotes': forms.Textarea(attrs={'style': 'width: 620px;', 'rows': 10}),
            'eroNotes': forms.Textarea(attrs={'style': 'width: 620px;', 'rows': 10}),
            'artNotes': forms.Textarea(attrs={'style': 'width: 620px;', 'rows': 10}),
        }
    
class SessionUssuriysk(models.Model):
    Day = models.OneToOneField(Day, on_delete=models.CASCADE,verbose_name="Day",related_name="UssuriyskDay",null=True)
    title = models.CharField(max_length=100)
    TimeBegin = models.IntegerField(default=0)
    TimeEnd = models.IntegerField(default=0)
    sysSessionRequest = models.IntegerField(default=0)
    eroSessionRequest = models.IntegerField(default=0)
    artSessionRequest = models.IntegerField(default=0)
    sysNotes = models.TextField("System Notes",max_length=2000, null=True, blank=True) #,validators=[MaxLengthValidator(1600)])
    eroNotes = models.TextField("eRosita Notes",max_length=2000, null=True, blank=True) #,validators=[MaxLengthValidator(1600)])
    artNotes = models.TextField("ART-XC Notes",max_length=2000, null=True, blank=True) #,validators=[MaxLengthValidator(1600)])
    def __unicode__(self):
        return self.title
    def __str__(self):
        return 'Session: Day '  + "%i" % (self.Day.DayNumber)

