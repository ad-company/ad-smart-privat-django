from django.contrib import admin
from .models import Absence, Schedule


class ScheduleAdmin(admin.ModelAdmin):
    """
    Simple, read-only list/search view of Rating Admin.
    """
    list_display = [
        'user_student',
        'user_tentor',
        'schedule',
        'mapel',
        'location',
        'mode',
        'active',
    ]

class AbsenceAdmin(admin.ModelAdmin):
    """
    Simple, read-only list/search view of Rating Admin.
    """
    list_display = [
        'schedule',
        'user_student',
        'user_tentor',
        'attend_student',
        'student_assign_date',
        'attend_tentor',
        'tentor_assign_date',
        'mode',
        'grade',
        'total_student',
        'created_at',
        'updated_at',
    ]

list_admin = []

admin.site.register(list_admin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Absence, AbsenceAdmin)
