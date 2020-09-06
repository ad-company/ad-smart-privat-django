from django.contrib import admin
from .models import (
    Students,
    Price,
    # Paid
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
#         'note',
#         'created_at',
#         'updated_at',
#     ]

class PriceAdmin(admin.ModelAdmin):
    """
    Simple, read-only list/search view of Rating Admin.
    """
    list_display = [
        'name',
        'mode',
        'price',
    ]

class StudentsAdmin(admin.ModelAdmin):
    """
    Simple, read-only list/search view of Rating Admin.
    """
    list_display = [
        'user',
        'name',
        'address',
        'phone',
        'schedule_1',
        'schedule_2',
        'schedule_3',
        'schedule_4',
        'schedule_5',
        'schedule_6',
        'grade',
        'total_student',
        'mode',
        'status',
    ]

list_admin = []

admin.site.register(list_admin)
admin.site.register(Students, StudentsAdmin)
admin.site.register(Price, PriceAdmin)
# admin.site.register(Paid, PaidAdmin)