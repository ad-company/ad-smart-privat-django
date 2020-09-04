from django.db.models import CharField
from django.db.models import TextField
from django.utils import timezone
from django.db import models as models
from django.contrib.auth.models import User

from main_register_tentor.models import Tentors
from main_register_student.models import Students

MODE = [
    ('online (remote)', 'Online (remote)'),
    ('offline', 'Offline')
]

GRADE = [
    ('SD 1', 'SD 1'),
    ('SD 2', 'SD 2'),
    ('SD 3', 'SD 3'),
    ('SD 4', 'SD 4'),
    ('SD 5', 'SD 5'),
    ('SD 6', 'SD 6'),
    ('SMP 7', 'SMP 7'),
    ('SMP 8', 'SMP 8'),
    ('SMP 9', 'SMP 9'),
    ('SMA 10', 'SMA 10'),
    ('SMA 11', 'SMA 11'),
    ('SMA 12', 'SMA 12'),
]

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
        # return '{}{}{}{}{}{}'.format(self.id)
        return 'id {} user_student {} user_tentor {} schedule {} mapel {} mode {} active {}'.format(
            self.id,
            self.user_student,
            self.user_tentor,
            self.schedule,
            self.mapel,
            self.mode,
            self.active,
        )

    def __unicode__(self):
        return (
            'user_student: {user_student} with user_tentor: {user_tentor} schedule {schedule} mapel {mapel} '
            'mode {mode} active {active}.'
        ).format(
            user_student=self.user_student,
            user_tentor=self.user_tentor,
            schedule=self.schedule,
            mapel=self.mapel,
            mode=self.mode,
            active=self.active,
        )

    class Meta:
        verbose_name_plural = 'Schedule'

class Absence(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    user_student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='user_student_absence', blank=True, null=True)
    user_tentor = models.ForeignKey(Tentors, on_delete=models.CASCADE, related_name='user_tentor_absence', blank=True, null=True)
    attend_student = models.BooleanField(null=False, default=False)
    student_assign_date = models.DateTimeField(blank=True, null=True, default=None)
    attend_tentor = models.BooleanField(null=False, default=False)
    tentor_assign_date = models.DateTimeField(blank=True, null=True, default=None)
    mode = models.CharField(max_length=250, choices=MODE, null=False, blank=False)
    grade = models.CharField(
        max_length=10,
        choices=GRADE,
        null=False,
        default=""
    )
    total_student = models.CharField(max_length=250, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return '{}'.format(self.schedule)

    class Meta:
        verbose_name_plural = 'Absence'
