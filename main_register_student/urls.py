from django.urls import path
from home.views import register_user
from main_register_student.views import (
    register_student_profile,
    # form,
    # porto_get
)

urlpatterns = [
    path ('', register_user, name='register_user'),
    path ('profile/u/<str:username>', register_student_profile, name='register_student_profile'),
    # path ('barang/<int:porto_id>', porto_get, name='porto_id')
]