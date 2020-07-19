from django.urls import path, include
from home.views import (
    base,
    register_user,
    profile_page
    # form,
    # porto_get
)

urlpatterns = [
    # Auth
    path ('', include('django.contrib.auth.urls')),

    path ('', base, name='base'),
    path ('register/<str:user_type>', register_user, name='register_user'),
    path ('profile', profile_page, name='profile_page'),
    # path ('add', form, name='form'),
    # path ('barang/<int:porto_id>', porto_get, name='porto_id')
]