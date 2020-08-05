from django.db.models import CharField
from django.db.models import TextField
from django.utils import timezone
from django.db import models as models
from django.contrib.auth.models import User

from main_register_tentor.models import Tentors
from main_register_student.models import Students


def photo_prove(instance, filename):
    return 'uploads/absence/absence_{}_{}_{}.jpg'.format(
        str(timezone.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')),
        instance.user.id,
        instance.user.username.replace(' ', '_')
    )

class Schedule(models.Model):
    user_student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='user_student')
    user_tentor = models.ForeignKey(Tentors, on_delete=models.CASCADE, related_name='user_tentor', blank=True, null=True)
    schedule = models.CharField(max_length=250, null=False)
    mapel = models.CharField(max_length=250, null=False)
    location = models.CharField(max_length=250, null=False)
    mode = models.CharField(max_length=250, null=False)
    active = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return '{}'.format(self.user_student)

    class Meta:
        verbose_name_plural = 'Schedule'

class Absence(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    attend_student = models.BooleanField(null=False, default=False)
    student_assign_date = models.DateTimeField(blank=True, null=True, default=None)
    attend_tentor = models.BooleanField(null=False, default=False)
    tentor_assign_date = models.DateTimeField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return '{}'.format(self.schedule)

    class Meta:
        verbose_name_plural = 'Absence'
