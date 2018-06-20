from django import template

register = template.Library()

@register.filter
def format00(value):
    return '{:02d}'.format(value)
