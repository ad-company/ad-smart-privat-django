import re
import base64
from datetime import datetime, date, time, timedelta

from django.db.models import Q
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
def payment_page(request, year=None):
    # Check if student or tentor
    user = request.user
    if user.is_staff == True: 
        if user.is_superuser == True:
            user_type = 'superuser'
        else:
            # Page is restricted for tentor
            user_type = 'tentor'
            return redirect('/')
    else:
        user_type = 'student'

    form = {}
    form['user_type'] = user_type

    # day, date, datetime & year
    if year == None:
        year = datetime.today().year
    year_min = datetime.combine(date(year, 1, 1), time.min)
    year_max = datetime.combine(date(year, 12, 31), time.max)
    form['year'] = year

    months = {}
    form['list_months'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for num, month in enumerate(form['list_months']):
        month_num = num + 1
        months[f'{month}_min'] = datetime.combine(date(year, month_num, 1), time.min)

        if month_num == 2:  # February
            months[f'{month}_max'] = datetime.combine(date(year, month_num, 28), time.max)

        elif month_num <= 7:  # January - July
            if month_num % 2 == 0:  # Even month
                months[f'{month}_max'] = datetime.combine(date(year, month_num, 30), time.max)
            elif month_num % 2 != 0:  # Odd month
                months[f'{month}_max'] = datetime.combine(date(year, month_num, 31), time.max)

        elif month_num > 7 and month_num <= 12:  # August - December
            if month_num % 2 != 0:  # Even month
                months[f'{month}_max'] = datetime.combine(date(year, month_num, 30), time.max)
            elif month_num % 2 == 0:  # Odd month
                months[f'{month}_max'] = datetime.combine(date(year, month_num, 31), time.max)

    # Price list
    price_sd = ['SD 1', 'SD 2', 'SD 3', 'SD 4', 'SD 5']
    price_sd_up = ['SD 6']
    price_smp = ['SMP 7', 'SMP 8']
    price_smp_up = ['SMP 9']
    price_sma = ['SMA 10', 'SMA 11']
    price_sma_up = ['SMA 12']

    # Student need
    if user_type == 'student':
        student = Students.objects.get(pk=user.id)
        form['user_student'] = student

        # Handler duplicate data
        all_absence = []

        for month in form['list_months']:
            form[f'{month}_list'] = 0
            form[f'{month}_total'] = 0

        for num, month in enumerate(form['list_months']):
            form['list_absence'] = Absence.objects.filter(
                Q(student_assign_date__range=[months[f'{month}_min'], months[f'{month}_max']]) | Q(tentor_assign_date__range=[months[f'{month}_min'], months[f'{month}_max']]),
                Q(attend_student=True) | Q(attend_tentor=True),
                user_student=student,
            ) # Get list per month

            # Loop absence for every month
            for absence in form['list_absence']:
                if absence not in all_absence:
                    # Price type
                    if absence.grade in price_sd:
                        name = 'SD 1-5'
                    elif absence.grade in price_sd_up:
                        name = 'SD 6'
                    elif absence.grade in price_smp:
                        name = 'SMP 7-8'
                    elif absence.grade in price_smp_up:
                        name = 'SMP 9'
                    elif absence.grade in price_sma:
                        name = 'SMA 10-11'
                    elif absence.grade in price_sma_up:
                        name = 'SMA 12'

                    # Price mode
                    if absence.mode == 'offline' or absence.mode == 'both':  # price of both is same as offline
                        mode = 'offline'
                    else:
                        mode = 'online (remote)'  # online (remote)

                    # Price normal
                    form['price'] = Price.objects.get(name=name, mode=mode).price

                    # Discount group
                    if absence.total_student == '1':
                        discount = 0
                    elif absence.total_student == '2':
                        discount = 10
                    elif absence.total_student == '3':
                        discount = 15
                    elif absence.total_student == '4':
                        discount = 20
                    else:
                        discount = 0
                    form['discount'] = f'{discount}%'

                    # Get Date Absence
                    try:
                        tentor_date = absence.tentor_assign_date
                    except AttributeError:
                        tentor_date = None
                    try:
                        student_date = absence.student_assign_date
                    except AttributeError:
                        student_date = None

                    created_at = absence.created_at.strftime('%B %d, %Y')
                    if tentor_date and student_date:
                        if tentor_date < student_date:
                            created_at = absence.tentor_assign_date.strftime("%B")
                        elif tentor_date > student_date:
                            created_at = absence.student_assign_date.strftime("%B")
                    elif tentor_date and not student_date:
                        created_at = absence.tentor_assign_date.strftime("%B")
                    elif not tentor_date and student_date:
                        created_at = absence.student_assign_date.strftime("%B")

                    form[f'{created_at}_total'] += int(form['price'] * float(absence.total_student) * float(100 - discount) / float(100))
                    form[f'{created_at}_list'] += 1

                    # Prevent duplicate data
                    all_absence.append(absence)

            # Disc 10% if more than 4 meet
            if form[f'{month}_list'] > 4:
                form[f'{month}_total'] = int(form[f'{month}_total'] * 90 / 100)

            # Paid & Notes
            form[f'{month}_paid'] = '-'  # auto no payment if no data
            form[f'{month}_note'] = '-'  # Auto no note for this month

            try:
                paid_notes = Paid.objects.get(user=user, month=month, year=int(year))
                form[f'{month}_paid'] = paid_notes.paid # Get paid status if there's any data

                if paid_notes.note:
                    form[f'{month}_note'] = paid_notes.note # Get note if there's any data
            except Paid.DoesNotExist:
                pass

    # Superuser need
    if user_type == 'superuser':
        # Handler duplicate data
        all_absence = []

        form['data_superuser'] = []
        students = Students.objects.filter(user__is_active=True)

        for num, student in enumerate(students):
            # Identity
            data = {}
            data['user_student'] = student
            
            # Absence filter
            absences = Absence.objects.filter(
                Q(student_assign_date__range=[year_min, year_max]) | Q(tentor_assign_date__range=[year_min, year_max]),
                Q(attend_student=True) | Q(attend_tentor=True),
                user_student=student,
            ) # Get all list of absence this year

            # Total monthly SD - SMA
            for month in form['list_months']: 
                data[f'{month}_count'] = 0
                data[f'{month}_total'] = 0

            # Loop absence for 1 year
            for absence in absences:
                if absence not in all_absence:
                    # Price type
                    if absence.grade in price_sd:
                        name = 'SD 1-5'
                    elif absence.grade in price_sd_up:
                        name = 'SD 6'
                    elif absence.grade in price_smp:
                        name = 'SMP 7-8'
                    elif absence.grade in price_smp_up:
                        name = 'SMP 9'
                    elif absence.grade in price_sma:
                        name = 'SMA 10-11'
                    elif absence.grade in price_sma_up:
                        name = 'SMA 12'
                    else:
                        name = None

                    # Price mode
                    if absence.mode == 'offline' or absence.mode == 'both':  # price of both is same as offline
                        mode = 'offline'
                    else:
                        mode = 'online (remote)'  # online (remote)

                    # Price normal
                    price = Price.objects.get(name=name, mode=mode).price

                    # Discount group
                    if absence.total_student == '1':
                        discount = 0
                    elif absence.total_student == '2':
                        discount = 10
                    elif absence.total_student == '3':
                        discount = 15
                    elif absence.total_student == '4':
                        discount = 20
                    else:
                        discount = 0
                    
                    # Total price
                    total = int(price * float(absence.total_student) * float(100 - discount) / float(100))

                    # Get Date Absence
                    try:
                        tentor_date = absence.tentor_assign_date
                    except AttributeError:
                        tentor_date = None
                    try:
                        student_date = absence.student_assign_date
                    except AttributeError:
                        student_date = None

                    created_at = absence.created_at.strftime('%B %d, %Y')
                    if tentor_date and student_date:
                        if tentor_date < student_date:
                            created_at = absence.tentor_assign_date.strftime("%B")
                        elif tentor_date > student_date:
                            created_at = absence.student_assign_date.strftime("%B")
                    elif tentor_date and not student_date:
                        created_at = absence.tentor_assign_date.strftime("%B")
                    elif not tentor_date and student_date:
                        created_at = absence.student_assign_date.strftime("%B")

                    # Add total
                    data[f'{created_at}_total'] += total
                    data[f'{created_at}_count'] += 1

                    # Prevent duplicate data
                    all_absence.append(absence)

            # Check discount & paid status
            for month in form['list_months']:
                # Disc 10% if more that 4 meet
                if data[f'{month}_count'] > 4:
                    data[f'{month}_total'] = int(data[f'{month}_total'] * 90 / 100)

                data[f'{month}_paid'] = False  # auto False if not paid
                if data[f'{month}_total'] == 0:
                    data[f'{month}_paid'] = '-'  # No data this month
                else:
                    paid = Paid.objects.filter(user=student.user, month=month, year=int(year), paid=True)
                    if paid:
                        data[f'{month}_paid'] = True  # paid

            form['data_superuser'].append(data)

    form['range_request'] = range(0, 11)
    return render(request,'payment.html', {'form':form})

# def porto_get(request, porto_id):
#     return render(request, 'stuff.html',{'Porto': Porto.objects.get(pk=porto_id) })
