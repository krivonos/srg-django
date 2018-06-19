from django.shortcuts import render
from django.http import HttpResponse
from plan.models import Day, SessionBearLakes, SessionBearLakesForm, SessionUssuriysk
from plan.models import LaunchDate
from django.http import HttpResponseRedirect
import datetime
from django.utils import timezone

# Create your views here. Berkeley

def index(request):
    all_bearlakes = SessionBearLakes.objects.all()
    return render(request,'plan/show_plan.html', {'bearlakes': all_bearlakes,})
    #return HttpResponse("Hello, world. You're at the polls index.")

def init_plan(request):
    return HttpResponse("Locked. Remove all days first, then remove this lock, and run again.")
    for myday in range(1,150):
        day = Day(DayNumber=myday)
        day.save()
        s1 = SessionBearLakes(Day=day,TimeBegin=1,TimeEnd=2)
        s1.save()
        s2 = SessionUssuriysk(Day=day,TimeBegin=1,TimeEnd=2)
        s2.save()
    return HttpResponse("Initiate plan.")
#        raise Http404
#    if (all_days)
#    return render(request,'plan/show_plan.html', {'days': all_days,})
    #return HttpResponse("Hello, world. You're at the polls index.")

def update_plan_dates(request):
    days=Day.objects.all()
    for myday in days:
        myday.date = LaunchDate+datetime.timedelta(days=myday.DayNumber)
        myday.save()
    return HttpResponse("The dates have been updated according to launch date.")

def show_Day(request,day):
    try:
        myday=Day.objects.get(DayNumber__exact=day)
    except:
        return HttpResponse("This Day was not found")
    return HttpResponse("Initiate plan.")
#        raise Http404
#    if (all_days)
#    return render(request,'plan/show_plan.html', {'days': all_days,})

def show_SessionBearLakes(request,day):
    try:
        session=SessionBearLakes.objects.get(Day__DayNumber__exact=day)
    except:
        return HttpResponse("This Day was not found")
    return render(request,'plan/show_session_bearlakes.html', {'session': session,})

def update_SessionBearLakes(request,day):
    try:
        session=SessionBearLakes.objects.get(Day__DayNumber__exact=day)
    except:
        return HttpResponse("This Day was not found")
    if request.method == 'POST': # If the form has been submitted...
        form = SessionBearLakesForm(request.POST,instance=session) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            t_begin=form.cleaned_data["TimeBegin"]
            t_end=form.cleaned_data["TimeEnd"]
            session_duration=t_end-t_begin
            new_form=form.save()
            return HttpResponseRedirect(new_form.get_absolute_url())
        else:
            return render(request,'plan/update_session_bearlakes.html', {'form':form})

    else:
        form = SessionBearLakesForm(instance=session)
        return render(request,'plan/update_session_bearlakes.html', {'form':form})
