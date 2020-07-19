import re
import base64

from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from django.contrib.auth.models import User

from logs.log import log_track
from main_register_student.models import Students
from main_register_student.forms import StudentForm
from home.decorators import check_recaptcha, profile_availability


@profile_availability
@check_recaptcha
@log_track
def register_student_profile(request, username):
    form = request.POST.copy()
    if request.method == "POST":
        if request.recaptcha_is_valid:
            # Prepare user profile
            form = request.POST.copy()
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
                if form[f'schedule_{num}'] in handler_schedule:
                    form[f'schedule_{num}'] = ''
                else:
                    handler_schedule.append(form[f'schedule_{num}'])
                form.pop(f'clock_{num}')

            address = '{}, {}'.format(form['address'], form['city'])

            # Register profile
            try:
                Students.objects.create(
                    user=form['user'],
                    name=form['name'],
                    gender=form['gender'],
                    parent_name=form['parent_name'],
                    address = address,
                    phone=form['phone'],
                    id_pic=request.FILES['id_pic'],
                    school=form['school'],
                    schedule_1=form['schedule_1'],
                    schedule_2=form['schedule_2'],
                    schedule_3=form['schedule_3'],
                    schedule_4=form['schedule_4'],
                    schedule_5=form['schedule_5'],
                    schedule_6=form['schedule_6'],
                    grade=form['grade'],
                    total_student=form['total_student']
                )
                
                messages.success(request, 'Profile completed! We will contact you soon!')
                return redirect('profile_page')  # call with name from url 'profile_page'
            except Exception:
                form['list'] = list(form.keys())

        else:
            form['list'] = list(form.keys())

    form = {}
    form['user_type'] = 'Student'
    form['range'] = range(1, 7)  # Range for loop schedule
    return render(request, 'student_profile.html',{'form': form })

# def porto_get(request, porto_id):
#     return render(request, 'stuff.html',{'Porto': Porto.objects.get(pk=porto_id) })
