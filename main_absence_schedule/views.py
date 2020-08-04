import re
from datetime import datetime, date, time, timedelta

from django.utils import timezone
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
from main_register_student.models import Students


@login_required
@profile_availability
@log_track
def absence(request):
    # Check if student or tentor
    user = request.user
    if user.is_staff == True:
        user_type = 'tentor'
    else:
        user_type = 'student'

    # day, date & datetime
    today_min = datetime.combine(date.today() - timedelta(1), time.min)
    today_max = datetime.combine(date.today() + timedelta(1), time.max)

    local_day = datetime.now().strftime("%A")
    local_date = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
    local_datetime = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')

    if local_day == 'Monday':
        day_id = 'senin'
    elif local_day == 'Tuesday':
        day_id = 'selasa'
    elif local_day == 'Wednesday':
        day_id = 'rabu'
    elif local_day == 'Thursday':
        day_id = 'kamis'
    elif local_day == 'Friday':
        day_id = 'jumat'
    elif local_day == 'Saturday':
        day_id = 'sabtu'
    elif local_day == 'Sunday':
        day_id = 'ahad'
    else:
        day_id = ''

    form = {}
    form['user_type'] = user_type

    if request.method == 'POST':
        # Preparation data absence
        regex_id = re.compile(r'schedule-id-(.*)\':')
        schedule_id = re.findall(regex_id, str(request.POST))
        schedule = Schedule.objects.get(pk=schedule_id[0])

        # Check if absence already exist
        absence_data = Absence.objects.filter(schedule=schedule, created_at__range=[today_min, today_max])

        if user_type == 'tentor':
            if not absence_data:
                # create if doesn't exist
                try:
                    Absence.objects.create(
                        schedule=schedule,
                        attend_tentor=True,
                        tentor_assign_date=local_datetime
                    )
                    messages.success(request, "Save absence tentor success!")
                except Exception:
                    messages.error(request, "Fail to submit absence. Please try again or contact administrator!")
            else:
                # Update from existing absence
                absence_data.update(attend_tentor=True, tentor_assign_date=local_datetime)
                messages.success(request, "Save absence tentor success!")

        elif user_type == 'student':
            if not absence_data:
                # create if doesn't exist
                try:
                    Absence.objects.create(
                        schedule=schedule,
                        attend_student=True,
                        student_assign_date=local_datetime
                    )
                    messages.success(request, "Save absence student success!")
                except Exception:
                    messages.error(request, "Fail to submit absence. Please try again or contact administrator!")
            else:
                # Update from existing absence
                absence_data.update(attend_student=True, student_assign_date=local_datetime)
                messages.success(request, "Save absence student success!")

    # Get rendering data absence for today
    form['schedule'] = []
    if user_type == 'tentor':
        tentor = Tentors.objects.get(pk=user.id)
        list_absence = Absence.objects.filter(schedule__user_tentor=tentor, schedule__schedule__contains=day_id, created_at__range=[today_min, today_max]).values_list('schedule', flat=True)  # Get list of absence by schedule id
        list_schedule = Schedule.objects.filter(schedule__contains=day_id, user_tentor=request.user.id, active=True)  # Get all schedule for day

        form['absence'] = Absence.objects.filter(schedule__user_tentor=tentor, schedule__schedule__contains=day_id, attend_tentor=False, created_at__range=[today_min, today_max])  # Get absence that already created today
        form['absence_done'] = Absence.objects.filter(schedule__user_tentor=tentor, schedule__schedule__contains=day_id, attend_tentor=True, created_at__range=[today_min, today_max]).order_by('-attend_student')  # Get absence that already done today

    elif user_type == 'student':
        student = Students.objects.get(pk=user.id)
        list_absence = Absence.objects.filter(schedule__user_student=student, schedule__schedule__contains=day_id, created_at__range=[today_min, today_max]).values_list('schedule', flat=True)  # Get list of absence by schedule id
        list_schedule = Schedule.objects.filter(schedule__contains=day_id, user_student=request.user.id, active=True)  # Get all schedule for day

        form['absence'] = Absence.objects.filter(schedule__user_student=student, schedule__schedule__contains=day_id, attend_student=False, created_at__range=[today_min, today_max])  # Get absence that already created today
        form['absence_done'] = Absence.objects.filter(schedule__user_student=student, schedule__schedule__contains=day_id, attend_student=True, created_at__range=[today_min, today_max]).order_by('-attend_tentor')  # Get absence that already done today

    # Check schedule that still not created today (prevent duplication)
    for num in range(0, len(list_schedule)):
        if list_schedule[num].id not in list_absence:
            form['schedule'].append(list_schedule[num])
    # form['range_request'] = range(0, len(form['schedule']))
    return render(request,'absence.html', {'form':form})

@login_required
@profile_availability
@log_track
def open_schedule(request):
    # Check if student or tentor
    user = request.user
    if user.is_staff == True:
        user_type = 'tentor'
    else:
        user_type = 'student'
    
    if request.method=='POST' and user_type == 'tentor':
        regex_id = re.compile(r'schedule-id-(.*)\':')
        schedule_id = re.findall(regex_id, str(request.POST))
        alignment = Schedule.objects.filter(pk=schedule_id[0])

        # Assign tentor for this job!
        alignment.update(user_tentor=Tentors.objects.get(pk=user.id), active=True)
        messages.success(request, "Alignment Schedule success! Lets catch up with student from phone!")

    form = {}
    form['user_type'] = user_type

    # Get rendering data schedule
    if user_type == 'tentor':
        form['schedules_request'] = Schedule.objects.filter(active=False)
    elif user_type == 'student':
        return redirect('/schedule')
    form['range_request'] = range(0, len(form['schedules_request']))
    return render(request,'open_schedule.html', {'form':form})

@login_required
@profile_availability
@log_track
def schedule(request):
    # Check if student or tentor
    user = request.user
    if user.is_staff == True:
        user_type = 'tentor'
    else:
        user_type = 'student'

    form = {}
    form['user_type'] = user_type

    # Get rendering data schedule
    if user_type == 'tentor':
        form['schedules_active'] = Schedule.objects.filter(user_tentor=request.user.id, active=True)
    elif user_type == 'student':
        form['schedules_active'] = Schedule.objects.filter(user_student=request.user.id)
    form['range_request'] = range(0, len(form['schedules_active']))
    return render(request,'my_schedule.html', {'form':form})

# def porto_get(request, porto_id):
#     return render(request, 'stuff.html',{'Porto': Porto.objects.get(pk=porto_id) })
