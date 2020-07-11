from django.urls import path
from .views import (
    register_student,
    # form,
    # porto_get
)

urlpatterns = [
    path ('', register_student, name='register_student'),
    # path ('barang/<int:porto_id>', porto_get, name='porto_id')
]