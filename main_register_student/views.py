from django.shortcuts import render, redirect

import json
import urllib

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

from .models import Students
from .forms import StudentForm
from .decorators import check_recaptcha


@check_recaptcha
def register_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid() and not messages.error:
            form.save()
            messages.success(request, 'Register success!')
            return redirect('base')  # call with name from url 'base'
    else:
        form = StudentForm()
    return render(request, 'form.html',{'form': form })

# def porto_get(request, porto_id):
#     return render(request, 'stuff.html',{'Porto': Porto.objects.get(pk=porto_id) })
