from django import template
from django.utils.safestring import mark_safe
from suit.config import get_config

register = template.Library()


@register.filter(name='conf_suit')
def conf_suit(name):
    value = get_config(name)
    return mark_safe(value) if isinstance(value, str) else value
