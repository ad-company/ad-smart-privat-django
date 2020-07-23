import re

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from logs.log import log_track
from home.decorators import check_recaptcha, profile_availability
from main_absence_schedule.models import Absence, Schedule
from main_absence_schedule.forms import AbsenceForm
from main_register_tentor.models import Tentors


@login_required
@check_recaptcha
@log_track
def absence(request):
    # Check if student or tentor
    user = User.objects.get(pk=request.user.id).is_staff
    if user == True:
        user = 'tentor'
    else:
        user = 'student'
    # if request.method == 'POST':
    #     Absence.objects.create(

    #     )

    form = {}
    form['range'] = range(1, 7)  # Range for loop schedule

    if user == 'tentor':
        form['schedules'] = Schedule.objects.filter(user_tentor=request.user.id)
    elif user == 'student':
        form['schedules'] = Schedule.objects.filter(user_student=request.user.id)
    return render(request,'absence.html', {'form':form})

@login_required
# @check_recaptcha
@log_track
def schedule(request):
    # Check if student or tentor
    user = User.objects.get(pk=request.user.id).is_staff
    if user == True:
        user = 'tentor'
    else:
        user = 'student'
    
    if request.method=='POST' and user == 'tentor':
        regex_id = re.compile(r'schedule-id-(.*)\':')
        schedule_id = re.findall(regex_id, str(request.POST))
        alignment = Schedule.objects.get(pk=schedule_id[0])

        # Assign tentor for this job!
        alignment.user_tentor = User.objects.get(pk=request.user.id)
        alignment.active = True
        alignment.save()
        messages.success(request, "Alignment Schedule success! Lets catch up with student from chat!")

    form = {}
    form['user_type'] = user

    # Get rendering data schedule
    if user == 'tentor':
        form['schedules_request'] = Schedule.objects.filter(active=False)
        form['schedules_active'] = Schedule.objects.filter(user_tentor=request.user.id, active=True)
        form['range_request'] = range(0, len(form['schedules_request']))
    elif user == 'student':
        form['schedules_wait'] = Schedule.objects.filter(user_student=request.user.id, active=False)
        form['schedules_active'] = Schedule.objects.filter(user_student=request.user.id, active=True)
    return render(request,'schedule.html', {'form':form})

# def porto_get(request, porto_id):
#     return render(request, 'stuff.html',{'Porto': Porto.objects.get(pk=porto_id) })
