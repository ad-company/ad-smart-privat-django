from django.urls import path, include
from home.views import (
    base,
    register_user,
    profile_page,
    about_page,
    reset_password,
    # form,
    # porto_get
)

urlpatterns = [
    # Auth
    path ('', include('django.contrib.auth.urls')),

    path ('', base, name='base'),
    path ('register/<str:user_type>', register_user, name='register_user'),
    path ('profile', profile_page, name='profile_page'),
    path ('about', about_page, name='about_page'),
    path ('reset-password', reset_password, name='reset-password'),
    # path ('add', form, name='form'),
    # path ('barang/<int:porto_id>', porto_get, name='porto_id')
]