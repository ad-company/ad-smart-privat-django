from django.urls import path, include
from .views import (
    absence,
    # form,
    # porto_get
)

urlpatterns = [
    path ('', absence, name='absence'),
    path ('', include('django.contrib.auth.urls')),
    # path ('add', form, name='form'),
    # path ('barang/<int:porto_id>', porto_get, name='porto_id')
]