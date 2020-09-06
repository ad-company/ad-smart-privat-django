from django.contrib import admin
from .models import (
    Tentors,
    Bank,
    Fee,
    # Paid,
)


# class PaidAdmin(admin.ModelAdmin):
#     """
#     Simple, read-only list/search view of Rating Admin.
#     """
#     list_display = [
#         'id',
#         'user',
#         'month',
#         'year',
#         'paid',
#         'created_at',
#         'updated_at',
#     ]

class FeeAdmin(admin.ModelAdmin):
    """
    Simple, read-only list/search view of CertificateId Admin.
    """
    list_display = [
        'name',
        'mode',
        'price',
    ]

class BankAdmin(admin.ModelAdmin):
    """
    Simple, read-only list/search view of CertificateId Admin.
    """
    list_display = [
        'bank_name',
        'bank_id',
        'updated_at',
    ]

class TentorsAdmin(admin.ModelAdmin):
    """
    Simple, read-only list/search view of CertificateId Admin.
    """
    list_display = [
        'user',
        'name',
        'phone',
        'account_name',
        'account_id',
        'bank',
        'bank_other',
        'university',
        'major',
        'status',
    ]

list_admin = []

admin.site.register(list_admin)
admin.site.register(Fee, FeeAdmin)
# admin.site.register(Paid, PaidAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(Tentors, TentorsAdmin)