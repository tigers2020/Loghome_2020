from django import template

register = template.Library()


@register.filter(name='clean')
def clean(value, arg):
    return value.replace(arg, ' ')
