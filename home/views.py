import re
import json
import urllib
import base64

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from logs.log import log_track
from home.models import Base
from home.forms import BaseForm
from home.decorators import cookie_management, check_recaptcha, profile_availability


def base(request):
    return render(request, 'content.html')

def validate_pass(request, password):
    if len(password) < 8:
        messages.error(request, "Make sure your password is at lest 8 letters")
    elif re.search('[0-9]',password) is None:
        messages.error(request, "Make sure your password has a number in it")
    else:
        return True

@check_recaptcha
@log_track
def register_user(request):
    # Get data list user already registered
    users = User.objects.values_list('username', flat=True)
    form = request.POST.copy()

    # Post Method
    if request.method == "POST":
        if request.recaptcha_is_valid:
            # Prepare user register
            _user, _pass, _email = request.POST['username'], request.POST['password'], request.POST['email']

            # Validate password
            validation = validate_pass(request, _pass)

            # Register user
            try:
                if validation:
                    User.objects.create_user(
                        username=_user,
                        password=_pass,
                        email=_email
                    )
                else:
                    raise Exception("Sorry, password not match with requirements.")
            except Exception:
                messages.error(request, 'Username or password is wrong, please try again.')
                form['list'] = list(form.keys())
                form['users'] = users
                return render(request, 'register_form.html',{'form': form })

            messages.success(request, 'Register success! Please fill this profile for contact')

            # Preparing profile.html
            form = {}
            form['range'] = range(1, 7)  # Range for loop schedule
            username = base64.b64encode('{}_secure'.format(_user).encode("utf-8"))
            response = redirect(
                'profile/u/{}'.format(username),
                {'form': form}
            )
            # response.set_cookie(key='username_ad', value=_user)
            return response

        else:
            # reCaptha not valid
            form['list'] = list(form.keys())

    # GET Method
    form = {}
    form['users'] = users
    return render(request, 'register_form.html',{'form': form })

# def porto_get(request, porto_id):
#     return render(request, 'stuff.html',{'Porto': Porto.objects.get(pk=porto_id) })
