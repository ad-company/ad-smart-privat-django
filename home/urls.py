from django.urls import path, include
from .views import (
    base,
    # form,
    # porto_get
)

urlpatterns = [
    path ('', base, name='base'),
    # path ('add', form, name='form'),
    # path ('barang/<int:porto_id>', porto_get, name='porto_id')
]