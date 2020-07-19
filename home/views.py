import json
import re
import urllib
import base64

from django.contrib import messages
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from logs.log import log_track
from home.models import Base
from home.forms import BaseForm
from home.decorators import check_recaptcha, profile_availability

from main_register_student.models import Students
from main_register_tentor.models import Tentors


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
def register_user(request, user_type=None):
    # Get data list user already registered
    users = User.objects.values_list('username', flat=True)
    form = request.POST.copy()

    # Logout user if already login
    if request.user.is_authenticated:
        logout(request)

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
                    if user_type == 'tentor':
                        is_staff = True
                    elif user_type == 'student':
                        is_staff = False
                    else:
                        raise Exception("Sorry, somenthing is wrong.")

                    email_exist = User.objects.filter(email=_email).first()
                    if email_exist:
                        messages.error(request, 'Email is used, please try again.')
                        raise Exception("Sorry, email is used.")
                    User.objects.create_user(
                        username=_user,
                        password=_pass,
                        email=_email,
                        is_staff=is_staff
                    )
                else:
                    messages.error(request, 'Username or password is wrong, please try again.')
                    raise Exception("Sorry, password not match with requirements.")
            except Exception:
                form['list'] = list(form.keys())
                form['users'] = users
                return render(request, 'register_form.html',{'form': form })

            messages.success(request, 'Register success! Please fill this profile for contact')

            # Preparing profile.html
            form = {}
            form['user_type'] = user_type
            form['range'] = range(1, 7)  # Range for loop schedule
            username = base64.b64encode('{}_secure'.format(_user).encode("utf-8"))
            response = redirect(
                '/{}/profile/u/{}'.format(user_type, username),
                {'form': form}
            )
            return response

        else:
            # reCaptha not valid
            form['list'] = list(form.keys())

    # GET Method
    form = {}
    form['user_type'] = user_type
    form['users'] = users
    return render(request, 'register_form.html',{'form': form })


@login_required
@log_track
def profile_page(request):
    profile = None

    # Change Photo
    # if request.method = "POST":

    try:
        user = User.objects.filter(username=request.user).first()
        if user.is_staff == False:  # Student
            profile = Students.objects.filter(user=user.id).first()
        else:
            if user.is_superuser == False:  # Tentor
                profile = Tentors.objects.filter(user_id=user.id).first()
            else:  # SuperUser
                pass
    except KeyError:
        pass

    return render(request, 'profile.html', {'profile': profile})

# def porto_get(request, porto_id):
#     return render(request, 'stuff.html',{'Porto': Porto.objects.get(pk=porto_id) })
