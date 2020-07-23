from django.contrib import admin
from .models import Absence


list_admin = [ Absence ]

admin.site.register(list_admin)
