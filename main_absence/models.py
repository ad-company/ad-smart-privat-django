from django.db.models import CharField
from django.db.models import TextField
from django.utils import timezone
from django.db import models as models

from main_register_tentor.models import Tentors

class Absence(models.Model):

    # judul = models.CharField(max_length=150, default='')
    # deskripsi = models.CharField(max_length=255, default='')
    # images = models.ImageField(upload_to="Media/img")
    # harga = models.IntegerField(default=0)
    # created_at = models.DateTimeField(auto_now_add=True, blank=True)
    # updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        # return self.judul
        return self.id

    class Meta:
        verbose_name_plural = 'Absence'