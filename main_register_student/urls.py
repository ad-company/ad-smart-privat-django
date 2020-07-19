from django.urls import path
from main_register_student.views import (
    register_student_profile,
    # form,
    # porto_get
)

urlpatterns = [
    path ('profile/u/<str:username>', register_student_profile, name='register_student_profile'),
    # path ('barang/<int:porto_id>', porto_get, name='porto_id')
]