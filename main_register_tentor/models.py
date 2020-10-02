from django.db.models import CharField
from django.db.models import TextField
from django.utils import timezone
from django.db import models as models
from django.contrib.auth.models import User

GENDER = [
    ('m', 'Male'),
    ('f', 'Female')
]

MODE = [
    ('online (remote)', 'Online'),
    ('offline', 'Offline')
]

# Note : (+) means group per +1 student
FEE_TYPE = [
    ('SD 1-5', 'SD 1-5'),
    ('SD 1-5+', 'SD 1-5+'),
    ('SD 6', 'SD 6'),
    ('SD 6+', 'SD 6+'),
    ('SMP 7-8', 'SMP 7-8'),
    ('SMP 7-8+', 'SMP 7-8+'),
    ('SMP 9', 'SMP 9'),
    ('SMP 9+', 'SMP 9+'),
    ('SMA 10-11', 'SMA 10-11'),
    ('SMA 10-11+', 'SMA 10-11+'),
    ('SMA 12', 'SMA 12'),
    ('SMA 12+', 'SMA 12+'),
]

MONTH = [
    ('January', 'January'),
    ('February', 'February'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December')
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

class Paid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_tentor')
    month = models.CharField(max_length=250, choices=MONTH, null=False, blank=False)
    year = models.IntegerField(null=False, blank=False)
    paid = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name_plural = 'Paid'

class Fee(models.Model):
    name = models.CharField(max_length=250, choices=FEE_TYPE, null=False, blank=False)
    mode = models.CharField(max_length=250, choices=MODE, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Fee'


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

    def __unicode__(self):
        return (
            'User: {user} with name {name} phone {phone} bank {bank} account name {account_name} '
            'account id {account_id} university {university} major {major} and status {status}.'
        ).format(
            user=self.user,
            name=self.name,
            phone=self.phone,
            bank=self.bank,
            account_name=self.account_name,
            account_id=self.account_id,
            university=self.university,
            major=self.major,
            status=self.status,
        )

    class Meta:
        verbose_name_plural = 'Tentor'

# class PassingGrade(models.Model):
#     user_tentor = models.ForeignKey(Tentors, on_delete=models.CASCADE, related_name='user_tentor_grade', blank=True, null=True)
#     score = models.IntegerField(null=True, blank=True, default=0)
#     passed = models.BooleanField(null=False, blank=False, default=False)
#     created_at = models.DateTimeField(auto_now_add=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True, blank=True)

#     def __str__(self):
#         return self.bank_name

#     class Meta:
#         verbose_name_plural = 'PassingGrade'