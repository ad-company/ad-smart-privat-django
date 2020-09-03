import re
import base64
from datetime import datetime, date, time, timedelta

from django.utils import timezone
from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from logs.log import log_track
from main_absence_schedule.models import Absence, Schedule
from main_register_student.models import Students, Price, Paid
from main_register_student.forms import StudentForm
from home.decorators import check_recaptcha, profile_availability


# @profile_availability
@check_recaptcha
@log_track
def register_student_profile(request, username):
    form = {}
    if request.method == "POST":
        form = request.POST.copy()
        if request.recaptcha_is_valid:
            # Prepare user profile
            username = re.compile(r"b'(.*)'").findall(username)
            form['user'] = User.objects.filter(
                username=base64.b64decode(username[0]).decode("utf-8").replace('_secure', '')
            ).first()

            handler_schedule = []
            for num in range(1, 7):
                # Change data schedule
                schedule = form[f'schedule_{num}']
                clock = form[f'clock_{num}']
                form[f'schedule_{num}'] = f"{schedule}_{clock}"
                if form[f'schedule_{num}'] in handler_schedule or form[f'schedule_{num}'] == '_':
                    form[f'schedule_{num}'] = None
                else:
                    handler_schedule.append(form[f'schedule_{num}'])
                form.pop(f'clock_{num}')

                # Change mapel
                form[f'mapel_{num}'] = form[f'mapel_{num}'] if form[f'mapel_{num}'] else None

            address = '{}, {}'.format(form['address'], form['city'])

            # Format phone delete '+' & replace to 62
            form['phone'].replace('+', '')
            if form['phone'][0] == '0':
                form['phone'] = '62{}'.format(form['phone'][1:])

            # Register profile
            try:
                student = Students.objects.create(
                    user=form['user'],
                    name=form['name'].title(),
                    gender=form['gender'],
                    parent_name=form['parent_name'].title(),
                    address=address,
                    phone=form['phone'],
                    school=form['school'],
                    schedule_1=form['schedule_1'],
                    schedule_2=form['schedule_2'],
                    schedule_3=form['schedule_3'],
                    schedule_4=form['schedule_4'],
                    schedule_5=form['schedule_5'],
                    schedule_6=form['schedule_6'],
                    mapel_1=form['mapel_1'],
                    mapel_2=form['mapel_2'],
                    mapel_3=form['mapel_3'],
                    mapel_4=form['mapel_4'],
                    mapel_5=form['mapel_5'],
                    mapel_6=form['mapel_6'],
                    grade=form['grade'],
                    total_student=form['total_student'],
                    mode=form['mode'],
                    # number_id=form['number_id'],
                    # id_pic=request.FILES['id_pic'],
                )

                try:
                    # Generate Schedule intiate
                    for num in range(1, 7):
                        if form[f'schedule_{num}']:
                            Schedule.objects.create(
                                user_student=student,
                                schedule=form[f'schedule_{num}'],
                                mapel=form[f'mapel_{num}'],
                                location=address,
                                mode=form['mode']
                            )
                    
                    messages.success(request, 'Profile completed! Our tentor will contact you soon. Get ready!!')
                    return redirect('profile_page')  # call with name from url 'profile_page'
                except Exception:
                    messages.error(request, 'Schedule failed to create. Please call administration.')
            except Exception:
                messages.error(request, 'Profile failed to create. Please try again or call administration.')
                form['list'] = list(form.keys())
    
    form['user_type'] = 'Student'
    form['range'] = range(1, 7)  # Range for loop schedule
    return render(request, 'student_profile.html',{'form': form })

@login_required
@profile_availability
@log_track
def payment_page(request):
    # Check if student or tentor
    user = request.user
    if user.is_staff == True and user.is_superuser == False:
        # Page is restricted for tentor
        user_type = 'tentor'
        return redirect('/')
    else:
        user_type = 'student'

    form = {}
    form['user_type'] = user_type
    student = Students.objects.get(pk=user.id)

    # day, date, datetime & year
    year = datetime.today().year
    month_min = datetime.combine(date(year, 1, 1), time.min)
    month_max = datetime.combine(date(year, 12, 31), time.max)
    list_months_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    form['list_months'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    form['year'] = year

    # Price list
    price_sd = ['SD 1', 'SD 2', 'SD 3', 'SD 4', 'SD 5']
    price_sd_up = ['SD 6']
    price_smp = ['SMP 7', 'SMP 8']
    price_smp_up = ['SMP 9']
    price_sma = ['SMA 10', 'SMA 11']
    price_sma_up = ['SMA 12']

    # Price type
    if student.grade in price_sd:
        name = 'SD 1-5'
    elif student.grade in price_sd_up:
        name = 'SD 6'
    elif student.grade in price_smp:
        name = 'SMP 7-8'
    elif student.grade in price_smp_up:
        name = 'SMP 9'
    elif student.grade in price_sma:
        name = 'SMA 10-11'
    elif student.grade in price_sma_up:
        name = 'SMA 12'

    # Price mode
    if student.mode == 'offline' or student.mode == 'both':  # price of both is same as offline
        mode = 'offline'
    else:
        mode = 'online (remote)'  # online (remote)

    # Discount group
    if student.total_student == '1':
        discount = 0
    elif student.total_student == '2':
        discount = 10
    elif student.total_student == '3':
        discount = 15
    elif student.total_student == '4':
        discount = 20
    else:
        discount = 0
    form['discount'] = f'{discount}%'

    form['user_student'] = student
    form['price'] = Price.objects.get(name=name, mode=mode).price
    form['list_absence'] = Absence.objects.filter(schedule__user_student=student, created_at__range=[month_min, month_max]) # Get all list of absence this year

    # Total group monthly
    for month in form['list_months']: 
        form[f'list_{month}'] = []

    for data in form['list_absence']:
        # Check what month data is it
        if data.created_at.month == list_months_num[0]: # January
            form[f"list_{form['list_months'][0]}"].append(data)
        elif data.created_at.month == list_months_num[1]: # February
            form[f"list_{form['list_months'][1]}"].append(data)
        elif data.created_at.month == list_months_num[2]: # March
            form[f"list_{form['list_months'][2]}"].append(data)
        elif data.created_at.month == list_months_num[3]: # April
            form[f"list_{form['list_months'][3]}"].append(data)
        elif data.created_at.month == list_months_num[4]: # May
            form[f"list_{form['list_months'][4]}"].append(data)
        elif data.created_at.month == list_months_num[5]: # June
            form[f"list_{form['list_months'][5]}"].append(data)
        elif data.created_at.month == list_months_num[6]: # July
            form[f"list_{form['list_months'][6]}"].append(data)
        elif data.created_at.month == list_months_num[7]: # August
            form[f"list_{form['list_months'][7]}"].append(data)
        elif data.created_at.month == list_months_num[8]: # September
            form[f"list_{form['list_months'][8]}"].append(data)
        elif data.created_at.month == list_months_num[9]: # October
            form[f"list_{form['list_months'][9]}"].append(data)
        elif data.created_at.month == list_months_num[10]: # November
            form[f"list_{form['list_months'][10]}"].append(data)
        elif data.created_at.month == list_months_num[11]: # December
            form[f"list_{form['list_months'][11]}"].append(data)

    for month in form['list_months']: 
        form[f'total_{month}'] = len(form[f'list_{month}']) * (form['price'] * float(student.total_student) * float(100 - discount) / float(100))
        form[f'paid_{month}'] = False  # auto False if not paid
        
        if form[f'total_{month}'] == 0:
            form[f'paid_{month}'] = '-'  # No data this month
        else:
            paid = Paid.objects.filter(user=user, month=month, year=int(year), paid=True)
            if paid:
                form[f'paid_{month}'] = True  # paid


    form['range_request'] = range(0, len(form['list_absence']))
    return render(request,'payment.html', {'form':form})

# def porto_get(request, porto_id):
#     return render(request, 'stuff.html',{'Porto': Porto.objects.get(pk=porto_id) })
