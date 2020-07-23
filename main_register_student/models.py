from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.db import models as models
from django.contrib.auth.models import User


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

GENDER = [
    ('m', 'Male'),
    ('f', 'Female')
]

def photo_id(instance, filename):
    return 'uploads/student/id/id_{}_{}.jpg'.format(
        instance.user.id,
        instance.user.username
    )

def photo_profile(instance, filename):
    return 'uploads/student/profile/profile_{}_{}.jpg'.format(
        instance.user.id,
        instance.user.username
    )

class Students(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False)
    gender = models.CharField(max_length=2, choices=GENDER, null=False)
    parent_name = models.CharField(max_length=250, null=False)
    address = models.CharField(max_length=250, null=False)
    phone = models.CharField(max_length=14, null=False)
    id_pic = models.ImageField('img', upload_to=photo_id, default='uploads/user-no-image.png')
    profile_pic = models.ImageField('img', upload_to=photo_profile)
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
    mode = models.CharField(max_length=150, null=False)
    user_type = models.CharField(max_length=100, editable=False, default="student")
    status = models.BooleanField(null=True, default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return '{}'.format(self.user)

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