from django.urls import path
from .views import (
    absence,
    # form,
    # porto_get
)

urlpatterns = [
    path ('', absence, name='absence'),
    # path ('add', form, name='form'),
    # path ('barang/<int:porto_id>', porto_get, name='porto_id')
]