from django.contrib import admin
from .models import (
    Tentors,
    Bank
)

class BankAdmin(admin.ModelAdmin):
    """
    Simple, read-only list/search view of CertificateId Admin.
    """
    list_display = [
        'bank_name',
        'bank_id',
        'updated_at',
    ]

list_admin = [ Tentors ]

admin.site.register(list_admin)
admin.site.register(Bank, BankAdmin)