from django.urls import path
from .views import (
    register_tentor,
    # form,
    # porto_get
)

urlpatterns = [
    path ('', register_tentor, name='register_tentor'),
    # path ('add', form, name='form'),
    # path ('barang/<int:porto_id>', porto_get, name='porto_id')
]