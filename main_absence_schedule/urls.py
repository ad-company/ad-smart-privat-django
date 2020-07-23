from django.urls import path
from .views import (
    absence,
    schedule,
    # form,
    # porto_get
)

urlpatterns = [
    path ('absence', absence, name='absence'),
    path ('schedule', schedule, name='schedule'),
    # path ('add', form, name='form'),
    # path ('barang/<int:porto_id>', porto_get, name='porto_id')
]