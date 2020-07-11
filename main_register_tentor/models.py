from django.db.models import CharField
from django.db.models import TextField
from django.utils import timezone
from django.db import models as models


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
    name = models.CharField(max_length=250, primary_key=True)
    email = models.CharField(max_length=100, null=False)
    phone = models.IntegerField(null=False)
    address = models.CharField(max_length=250, null=False)
    account_name = models.CharField(max_length=250, null=False)
    account_id = models.IntegerField(null=False)
    bank_name = models.OneToOneField(Bank, on_delete=models.CASCADE)
    university = models.CharField(max_length=150, null=False)
    major = models.CharField(max_length=100, null=False)
    user_type = models.CharField(max_length=100, editable=False, default="tentor")
    status = models.BooleanField(null=True, default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Tentor'
