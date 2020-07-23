import re
import base64
import requests

from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from logs.log import log_track
from main_register_tentor.models import Tentors, Bank
from main_register_tentor.forms import TentorForm
from home.decorators import check_recaptcha, profile_availability


# @profile_availability
@check_recaptcha
@log_track
def register_tentor_profile(request, username):
    form = request.POST.copy()
    banks = Bank.objects.all()

    if request.method == "POST":
        if request.recaptcha_is_valid:
            # Prepare user profile
            form = request.POST.copy()
            username = re.compile(r"b'(.*)'").findall(username)
            form['user'] = User.objects.filter(
                username=base64.b64decode(username[0]).decode("utf-8").replace('_secure', '')
            ).first()

            address = '{}, {}'.format(form['address'], form['city'])
            bank = Bank.objects.filter(bank_name=form['bank']).first()

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
                    number_id=form['number_id'],
                    id_pic=request.FILES['id_pic'],
                )

                messages.success(request, 'Profile completed! We will contact you soon!')
                return redirect('profile_page')  # call with name from url 'profile_page'
            except Exception:
                form['list'] = list(form.keys())

        else:
            form['list'] = list(form.keys())

    form = {}
    form['user_type'] = 'Tentor'
    form['banks'] = banks
    return render(request, 'tentor_profile.html',{'form': form })

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
        # question.append(response['question'])
        # choices.append(response['choices'])

    tests = {}
    tests['question'] = response['question']
    tests['choices'] = response['choices']
    return render(request, 'tentor_test.html', { 'tests': tests })

# def porto_get(request, porto_id):
#     return render(request, 'stuff.html',{'Porto': Porto.objects.get(pk=porto_id) })
