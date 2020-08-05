import re
import base64

from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from django.contrib.auth.models import User

from logs.log import log_track
from main_absence_schedule.models import Schedule
from main_register_student.models import Students
from main_register_student.forms import StudentForm
from home.decorators import check_recaptcha, profile_availability


# @profile_availability
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
                if form[f'schedule_{num}'] in handler_schedule or form[f'schedule_{num}'] == '_':
                    form[f'schedule_{num}'] = None
                else:
                    handler_schedule.append(form[f'schedule_{num}'])
                form.pop(f'clock_{num}')

                # Change mapel
                form[f'mapel_{num}'] = form[f'mapel_{num}'] if form[f'mapel_{num}'] else None

            address = '{}, {}'.format(form['address'], form['city'])

            # Register profile
            try:
                student = Students.objects.create(
                    user=form['user'],
                    name=form['name'].title(),
                    gender=form['gender'],
                    parent_name=form['parent_name'].title(),
                    address=address,
                    phone=form['phone'],
                    id_pic=request.FILES['id_pic'],
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
                    mode=form['mode']
                )

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
                form['list'] = list(form.keys())

        else:
            form['list'] = list(form.keys())

    form = {}
    form['user_type'] = 'Student'
    form['range'] = range(1, 7)  # Range for loop schedule
    return render(request, 'student_profile.html',{'form': form })

# def porto_get(request, porto_id):
#     return render(request, 'stuff.html',{'Porto': Porto.objects.get(pk=porto_id) })
