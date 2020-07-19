import datetime
import requests
from functools import wraps

from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User


# def cookie_management(response, key, value, days_expire = 7):
#     if days_expire is None:
#         max_age = 365 * 24 * 60 * 60  #one year
#     else:
#         max_age = days_expire * 24 * 60 * 60 
#     expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
#     response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

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
        # Check username AD Smart Privat
        request.COOKIES.get('username_ad')
        if request.COOKIES['username_ad']:
            try:
                User.objects.get(username=request.COOKIES['username_ad'])
            except User.DoesNotExist:
                messages.error(request, 'Username doesn\'t exist. Please register first.')
                return redirect('register_student')
        return view_func(request, *args, **kwargs)
    return _wrapped_view