from django.contrib import admin
from .models import Absence, Schedule


list_admin = [ Absence, Schedule ]

admin.site.register(list_admin)
