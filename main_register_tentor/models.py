from django.db.models import CharField
from django.db.models import TextField
from django.utils import timezone
from django.db import models as models
from django.contrib.auth.models import User

GENDER = [
    ('m', 'Male'),
    ('f', 'Female')
]


def photo_id(instance, filename):
    return 'uploads/tentor/id/id_{}_{}.jpg'.format(
        instance.user.id,
        instance.user.username.replace(' ', '_')
    )

def photo_profile(instance, filename):
    return 'uploads/tentor/profile/profile_{}_{}.jpg'.format(
        instance.user.id,
        instance.user.username.replace(' ', '_')
    )

class Bank(models.Model):
    bank_name = models.CharField(max_length=250, primary_key=True)
    bank_id = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.bank_name

    class Meta:
        verbose_name_plural = 'Bank'


class Tentors(models.Model):
    user = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False)
    gender = models.CharField(max_length=2, choices=GENDER, null=False)
    phone = models.CharField(max_length=15, null=False)
    address = models.CharField(max_length=250, null=False)
    account_name = models.CharField(max_length=250, null=False)
    account_id = models.CharField(max_length=20, null=False)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    bank_other = models.CharField(max_length=20, null=True, blank=True, default=None)
    university = models.CharField(max_length=150, null=False)
    major = models.CharField(max_length=100, null=False)
    number_id = models.CharField(max_length=100, null=False, default='00')
    id_pic = models.ImageField('img', null=True, blank=True, upload_to=photo_id, default='uploads/user-no-image.png')
    profile_pic = models.ImageField('img', null=True, blank=True, upload_to=photo_profile, default='uploads/user-no-image.png')
    user_type = models.CharField(max_length=100, editable=False, default="tentor")
    status = models.BooleanField(null=True, default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name_plural = 'Tentor'
