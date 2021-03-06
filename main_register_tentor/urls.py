from django.urls import path
from main_register_tentor.views import (
    register_tentor_profile,
    fee_page,
    tentor_test,
    # form,
    # porto_get
)

urlpatterns = [
    path ('profile/u/<str:username>', register_tentor_profile, name='register_tentor_profile'),
    path ('fee/<int:year>', fee_page, name='fee_page'),
    path ('test', tentor_test, name='tentor_test'),
    # path ('add', form, name='form'),
    # path ('barang/<int:porto_id>', porto_get, name='porto_id')
]