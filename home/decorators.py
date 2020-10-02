import base64
import datetime
import requests
from functools import wraps

from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.defaulttags import register

from main_register_student.models import Students
from main_register_tentor.models import (
    Tentors,
    # PassingGrade
)

# def cookie_management(response, key, value, days_expire = 7):
#     if days_expire is None:
#         max_age = 365 * 24 * 60 * 60  #one year
#     else:
#         max_age = days_expire * 24 * 60 * 60 
#     expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
#     response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

# FIlter month for template
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def profile_availability(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Preparation redirect registration_form
        form = {}
        form['range'] = range(1, 7)  # Range for loop schedule

        # Check username profile availability
        if request.user.username:
            user_encode = base64.b64encode('{}_secure'.format(request.user.username).encode("utf-8"))

            try:
                user = User.objects.get(username=request.user.username)
            except User.DoesNotExist:
                messages.error(request, 'Username doesnt exist. Please register first.')
                return redirect('register_student')

            # Check data student or tentor
            if user.is_staff == False:  # Student
                profile = Students.objects.filter(user=user.id).first()
                if not profile:
                    #If profile dowsn't exist, redirect to profile as student
                    form['user_type'] = 'student'
                    messages.error(request, 'Please help us fill this profile first.')
                    return redirect(
                        '/{}/profile/u/{}'.format('student', user_encode),
                        {'form': form}
                    )

            else:
                if user.is_superuser == False:  # Tentor
                    form['user_type'] = 'tentor'
                    profile = Tentors.objects.filter(user_id=user.id).first()
                    # passing_grade = PassingGrade.objects.filter(user_tentor=profile).first()
                    if not profile:
                        #If profile dowsn't exist, redirect to profile as tentor
                        messages.error(request, 'Please help us fill this profile first.')
                        return redirect(
                            '/{}/profile/u/{}'.format('tentor', user_encode),
                            {'form': form}
                        )
                    # if passing_grade:
                    #     if not passing_grade.passed:
                    #         messages.error(request, 'We will review your result, please contact administrator +62 822-3326-9549.')
                    # else:
                    #     messages.error(request, 'We will review result, please get this test exam.')
                    #     return redirect(
                    #         '/tentor/test',
                    #         {'form': form}
                    #     )

        return view_func(request, *args, **kwargs)
    return _wrapped_view