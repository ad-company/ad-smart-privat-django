# from mongoengine import Document, EmbeddedDocument, fields
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.db import models as models
from django.contrib.auth.models import User
# from djongo import models as mongo_models
# from json_field import JSONField
# import jsonfield


DAYS = [
        ('senin', 'Senin'),
        ('selasa', 'Selasa'),
        ('rabu', 'Rabu'),
        ('kamis', 'Kamis'),
        ('jumat', 'Jumat'),
        ('sabtu', 'Sabtu'),
        ('minggu', 'Minggu'),
]

GRADE = [
    ('SD', 'SD'),
    ('SMP', 'SMP'),
    ('SMA', 'SMA')
]

HOUR = [
    ('09.00', '09.00'),
    ('10.00', '10.00'),
    ('11.00', '11.00'),
    ('12.00', '12.00'),
    ('13.00', '13.00'),
    ('14.00', '14.00'),
    ('15.00', '15.00'),
    ('16.00', '16.00'),
    ('17.00', '17.00'),
    ('18.00', '18.00'),
    ('19.00', '19.00')
]


class Students(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False)
    parent_name = models.CharField(max_length=250, null=False)
    address = models.CharField(max_length=250, null=False)
    phone = models.CharField(max_length=14, null=False)
    schedule_1 = models.CharField(max_length=20, null=False)
    schedule_2 = models.CharField(max_length=20)
    schedule_3 = models.CharField(max_length=20)
    schedule_4 = models.CharField(max_length=20)
    schedule_5 = models.CharField(max_length=20)
    schedule_6 = models.CharField(max_length=20)
    grade = models.CharField(
        max_length=3,
        choices=GRADE,
        null=False,
        default=""
    )
    total_student = models.CharField(max_length=250, null=False)
    school = models.CharField(max_length=150, null=False)
    user_type = models.CharField(max_length=100, editable=False, default="student")
    status = models.BooleanField(null=True, default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Student'


# class Details(models.Model):
#     # name = models.ForeignKey(Students, on_delete=models.CASCADE)
#     label = mongo_models.CharField(max_length=14, null=False)
    

#     def __str__(self):
#         return self.label

#     class Meta:
#         using = 'mongodb'
#         verbose_name_plural = 'Schedule'