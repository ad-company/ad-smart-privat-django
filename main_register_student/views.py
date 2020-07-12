import re
import json
import urllib
from logs.log import log_track

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Students
from .forms import StudentForm
from .decorators import check_recaptcha


def validate_pass(request, password):
    if len(password) < 8:
        messages.error(request, "Make sure your password is at lest 8 letters")
    elif re.search('[0-9]',password) is None:
        messages.error(request, "Make sure your password has a number in it")
    elif re.search('[A-Z]',password) is None: 
        messages.error(request, "Make sure your password has a capital letter in it")
    else:
        return True

@check_recaptcha
def register_student(request):
    log_track('/register-student')
    # Get data list user already registered
    users = User.objects.values_list('username', flat=True)

    if request.method == "POST":
        if request.recaptcha_is_valid:
            # Prepare user register
            _user, _pass, _email = request.POST['username'], request.POST['password'], request.POST['email']

            # Validate password
            validation = validate_pass(request, _pass)

            # Register user
            try:
                if validation:
                    user = User.objects.create_user(
                            username=_user,
                            password=_pass,
                            email=_email
                        )
                else:
                    raise Exception("Sorry, password not match with requirements.")
            except Exception:
                messages.error(request, 'Username or password is wrong, please try again.')
                form = request.POST.copy()
                form['list'] = list(form.keys())
                form['users'] = users
                return render(request, 'form.html',{'form': form })

            # Prepare user profile
            post = request.POST.copy()
            post.pop('username')
            post.pop('password')
            post.pop('email')
            post['user'] = user.id

            handler_schedule = []
            for num in range(1, 7):
                # Change data schedule
                schedule = post[f'schedule_{num}']
                clock = post[f'clock_{num}']
                post[f'schedule_{num}'] = f"{schedule}_{clock}]"
                if post[f'schedule_{num}'] in handler_schedule:
                    post.pop(f'schedule_{num}')
                else:
                    handler_schedule.append(post[f'schedule_{num}'])
            request.POST = post

            # Register profile
            form = StudentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Register success!\n We\'ll contact you soon!')
                return redirect('base')  # call with name from url 'base'
        else:
            form = request.POST.copy()
            form['list'] = list(form.keys())
    else:
        form = {}
        # form['form'] = StudentForm()

    form['users'] = users
    form['range'] = range(1, 7)  # Range for loop schedule
    return render(request, 'form.html',{'form': form })

# def porto_get(request, porto_id):
#     return render(request, 'stuff.html',{'Porto': Porto.objects.get(pk=porto_id) })
