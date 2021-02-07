from django import template
from datetime import datetime

register = template.Library()

@register.filter
def get_year(diff):
    now = datetime.now()
    return now.year + int(diff)
