from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def is_future_date(date):
    return date >= timezone.now()
