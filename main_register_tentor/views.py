import re
import base64
import requests
from datetime import datetime, date, time, timedelta

from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from logs.log import log_track
from main_absence_schedule.models import Absence, Schedule
from main_register_tentor.models import Tentors, Bank, Fee, Paid
from main_register_tentor.forms import TentorForm
from home.decorators import check_recaptcha, profile_availability


@check_recaptcha
@log_track
def register_tentor_profile(request, username):
    form = {}
    
    if request.method == "POST":
        form = request.POST.copy()
        if request.recaptcha_is_valid:
            # Prepare user profile
            username = re.compile(r"b'(.*)'").findall(username)
            form['user'] = User.objects.filter(
                username=base64.b64decode(username[0]).decode("utf-8").replace('_secure', '')
            ).first()

            address = '{}, {}'.format(form['address'], form['city'])
            bank = Bank.objects.filter(bank_name=form['bank']).first()

            # Format phone delete '+' & replace to 62
            form['phone'].replace('+', '')
            if form['phone'][0] == '0':
                form['phone'] = '62{}'.format(form['phone'][1:])

            # Register profile
            try:
                Tentors.objects.create(
                    user=form['user'],
                    name=form['name'].title(),
                    gender=form['gender'],
                    phone=form['phone'],
                    address=address,
                    account_name=form['account_name'],
                    account_id=form['account_id'],
                    bank=bank,
                    bank_other=form['bank_other'],
                    university=form['university'],
                    major=form['major'],
                    # number_id=form['number_id'],
                    # id_pic=request.FILES['id_pic'],
                )

                messages.success(request, 'Profile completed! We will contact you soon!')
                return redirect('profile_page')  # call with name from url 'profile_page'
            except Exception:
                messages.error(request, 'Profile failed to create. Please try again or call administration.')
                form['list'] = list(form.keys())

    form['user_type'] = 'Tentor'
    form['banks'] = Bank.objects.all()
    return render(request, 'tentor_profile.html',{'form': form })

@profile_availability
@login_required
@log_track
def fee_page(request, year):
    # Check if student, tentor, or superuser
    user = request.user
    if user.is_staff == True:
        if user.is_superuser:
            user_type = 'superuser'
        else:
            user_type = 'tentor'
    else:
        # Page is restricted for student
        user_type = 'student'
        return redirect('/')

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

    # Tentor need
    if user_type == 'tentor':
        tentor = Tentors.objects.get(pk=user.id)
        form['user_tentor'] = tentor

        # Handler duplicate data
        all_absence = []

        # Total monthly SD - SMA
        for num, month in enumerate(form['list_months']):
            form[f'{month}_SD_1_5'] = 0
            form[f'{month}_SD_6'] = 0
            form[f'{month}_SMP_7_8'] = 0
            form[f'{month}_SMP_9'] = 0
            form[f'{month}_SMA_10_11'] = 0
            form[f'{month}_SMA_12'] = 0
            form[f'{month}_count'] = 0
            form[f'{month}_total_fee'] = 0

        for num, month in enumerate(form['list_months']):
            # Absence filter
            form['list_absence'] = Absence.objects.filter(
                Q(student_assign_date__range=[months[f'{month}_min'], months[f'{month}_max']]) | Q(tentor_assign_date__range=[months[f'{month}_min'], months[f'{month}_max']]),
                Q(attend_student=True) | Q(attend_tentor=True),
                user_tentor=tentor,
            ) # Get all list of absence this year

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
                    else:
                        name = None

                    # Fee mode
                    if absence.mode == 'offline' or absence.mode == 'both':  # price of both is same as offline
                        mode = 'offline'
                    else:
                        mode = 'online (remote)'  # online (remote)

                    # Fee normal
                    form['fee'] = Fee.objects.get(name=name, mode=mode).price

                    # Fee Additional Individu
                    name_addition = name + '+'
                    if int(absence.total_student) == 1:
                        addition = 0
                    # Fee Additional group
                    elif int(absence.total_student) == 2:
                        addition = Fee.objects.get(name=name_addition, mode=mode).price
                    elif int(absence.total_student) == 3:
                        addition = Fee.objects.get(name=name_addition, mode=mode).price * 2
                    elif int(absence.total_student) == 4:
                        addition = Fee.objects.get(name=name_addition, mode=mode).price * 3
                    else:
                        addition = 0

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

                    # Count Total Fee
                    form[f'{created_at}_total_fee'] += form['fee'] + addition

                    name_replace = name.replace(' ', '_').replace('-', '_')
                    form[f'{created_at}_{name_replace}'] += 1
                    form[f'{created_at}_paid'] = False  # auto False if not paid
                    
                    if form[f'{created_at}_total_fee'] == 0:
                        form[f'{created_at}_paid'] = '-'  # No data this month
                    else:
                        paid = Paid.objects.filter(user=user, month=created_at, year=int(year), paid=True)
                        if paid:
                            form[f'{created_at}_paid'] = True  # paid

                    # Prevent duplicate data
                    all_absence.append(absence)

            # # Get total all count per month
            # form[f'{month}_count'] = form[f'{month}_SD_1_5']
            # + form[f'{month}_SD_6']
            # + form[f'{month}_SMP_7_8']
            # + form[f'{month}_SMP_9']
            # + form[f'{month}_SMA_10_11']
            # + form[f'{month}_SMA_12']
            # print(form[f'{month}_count'], month)
            # print(form[f'{month}_SD_1_5'])
            # print(form[f'{month}_SD_6'])
            # print(form[f'{month}_SMP_7_8'])
            # print(form[f'{month}_SMP_9'])
            # print(form[f'{month}_SMA_10_11'])
            # print(form[f'{month}_SMA_12'])
    # End of tentor neeed

    # Superuser need
    if user_type == 'superuser':
        # Handler duplicate data
        all_absence = []

        form['data_superuser'] = []
        tentors = Tentors.objects.filter(user__is_active=True)

        for num, tentor in enumerate(tentors):
            # Identity
            data = {}
            data['user_tentor'] = tentor
            
            # Absence filter
            absences = Absence.objects.filter(
                Q(student_assign_date__range=[year_min, year_max]) | Q(tentor_assign_date__range=[year_min, year_max]),
                Q(attend_student=True) | Q(attend_tentor=True),
                user_tentor=tentor,
            ) # Get all list of absence this year

            # Total monthly SD - SMA
            for month in form['list_months']: 
                data[f'{month}_total'] = 0
                data[f'{month}_count'] = 0
            
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

                    # Fee mode
                    if absence.mode == 'offline' or absence.mode == 'both':  # price of both is same as offline
                        mode = 'offline'
                    else:
                        mode = 'online (remote)'  # online (remote)

                    # Fee normal
                    fee = Fee.objects.get(name=name, mode=mode).price

                    # Fee Additional Individu
                    name_addition = name + '+'
                    if int(absence.total_student) == 1:
                        addition = 0
                    # Fee Additional group
                    elif int(absence.total_student) == 2:
                        addition = Fee.objects.get(name=name_addition, mode=mode).price
                    elif int(absence.total_student) == 3:
                        addition = Fee.objects.get(name=name_addition, mode=mode).price * 2
                    elif int(absence.total_student) == 4:
                        addition = Fee.objects.get(name=name_addition, mode=mode).price * 3
                    else:
                        addition = 0

                    # Count Total Fee
                    fee += addition

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

                    # Add fee
                    data[f'{created_at}_total'] += fee
                    data[f'{created_at}_count'] += 1

                    # Prevent duplicate data
                    all_absence.append(absence)

            # Check paid status
            for month in form['list_months']: 
                data[f'{month}_paid'] = False  # auto False if not paid
                
                if data[f'{month}_total'] == 0:
                    data[f'{month}_paid'] = '-'  # No data this month
                else:
                    paid = Paid.objects.filter(user=tentor.user, month=month, year=int(year), paid=True)
                    if paid:
                        data[f'{month}_paid'] = True  # paid

            form['data_superuser'].append(data)
    # End of superuser need

    form['range_request'] = range(0, 11)
    return render(request,'fee.html', {'form':form})

@profile_availability
@login_required
@log_track
def tentor_test(request):
    url = "https://studycounts.com/api/v1/arithmetic/simple.json?difficulty=advanced"

    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMGNlOGEyY2MxODkyNGQ2ZTY5ZjQ5Y2U5MDQ5YWQ1N2VlMTU0ZjlhZDViMWQwY2I5NzAwYTE0ZjcyZjU0OTE1MTc5ZDQwMTk3MzYyMWM1M2MiLCJpYXQiOjE1OTIyODEwMzAsIm5iZiI6MTU5MjI4MTAzMCwiZXhwIjoxNjIzODE3MDMwLCJzdWIiOiI5MDgiLCJzY29wZXMiOltdfQ.r3M45IkPlLCVXVi680EN_sHYDwDNl8GAGumVL6C7qBPW-n0m9tLczfi52lCEsRpZYcUcY8tmj_41-0OSvBqdDYwJuacDyYWqgqzPBuOrk4Aa9HI354gWXawntJLNagXrqpeh6INsYE5n8bm0kYodKXfYeY04Bux28duv6B6Qon3XtHNMNGtBv27N7bHQ6zloSB025CeXCSbHkQ3S2E9mMEy13TeIbhRI9lmnXNXlFgQR_aUoCi6jC5M8kPdWsqrd-ggkCTPWUL0Lz4qtDwBhe5PrgzDY_yOZO-3clwC77HrhiIAkfBzEQ5AMK3oOb9RL9n4nDFhn9uQzOVbBG0xDH6iRWcRYxolnOs1rScjA0adIFqhwFmg2m0JfMGKwnIS1w4TE701iwy_9eRvdua14QUPEAeaFfjRjRm-QICjp4myck17XTMAME0cv73W_FL5dvHw7Z2nZg5mFO9J7PJri-ukiArR66NB66sE2tkCa_5LCKRfZRweWX1Xp5MsEijRlj0iDGE1MAhDmq0eWMw1wOq0BMl5kHPsPfSJ5cRak5R7McoTU05dyFmFhUVLO_LNayDdj4BWl6CFQXfBp-eCIYcxI17dyibK3REbl-nAHConfR9jl7xOl9RoV0iJXFpx3PB6omWedjBsP6XZ-bFLxkw3DAEVF1Jj8lj9HPwb_DVU'
    }

    question = []
    choices = []
    response = requests.request("GET", url, headers=headers, data = {}).json()
    # if response['question'] not in question and response['choices'] not in choices:
    #     question.append(response['question'])
    #     choices.append(response['choices'])

    tests = {}
    tests['question'] = response['question']
    tests['choices'] = response['choices']
    return render(request, 'tentor_test.html', { 'tests': tests })

# def porto_get(request, porto_id):
#     return render(request, 'stuff.html',{'Porto': Porto.objects.get(pk=porto_id) })
