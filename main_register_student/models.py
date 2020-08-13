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

GENDER = [
    ('m', 'Male'),
    ('f', 'Female')
]

def photo_id(instance, filename):
    return 'uploads/student/id/id_{}_{}.jpg'.format(
        instance.user.id,
        instance.user.username.replace(' ', '_')
    )

def photo_profile(instance, filename):
    return 'uploads/student/profile/profile_{}_{}.jpg'.format(
        instance.user.id,
        instance.user.username.replace(' ', '_')
    )

class Students(models.Model):
    user = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False)
    gender = models.CharField(max_length=2, choices=GENDER, null=False)
    parent_name = models.CharField(max_length=250, null=False)
    address = models.CharField(max_length=250, null=False)
    phone = models.CharField(max_length=14, null=False)
    #number_id = models.CharField(max_length=100, null=True, blank=True, default='00')
    id_pic = models.ImageField('img', null=True, blank=True, upload_to=photo_id, default='uploads/user-no-image.png')
    profile_pic = models.ImageField('img', null=True, blank=True, upload_to=photo_profile, default='uploads/user-no-image.png')
    schedule_1 = models.CharField(max_length=20, null=False)
    schedule_2 = models.CharField(max_length=20, null=True, blank=True, default=None)
    schedule_3 = models.CharField(max_length=20, null=True, blank=True, default=None)
    schedule_4 = models.CharField(max_length=20, null=True, blank=True, default=None)
    schedule_5 = models.CharField(max_length=20, null=True, blank=True, default=None)
    schedule_6 = models.CharField(max_length=20, null=True, blank=True, default=None)
    mapel_1 = models.CharField(max_length=20, null=False)
    mapel_2 = models.CharField(max_length=20, null=True, blank=True, default=None)
    mapel_3 = models.CharField(max_length=20, null=True, blank=True, default=None)
    mapel_4 = models.CharField(max_length=20, null=True, blank=True, default=None)
    mapel_5 = models.CharField(max_length=20, null=True, blank=True, default=None)
    mapel_6 = models.CharField(max_length=20, null=True, blank=True, default=None)
    grade = models.CharField(
        max_length=10,
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