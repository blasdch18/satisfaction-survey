from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def number(value, arg='int'):
    try:
        if arg == 'int' or arg == 'integer':
            value = int(float(value))
        elif arg == 'float':
            value = float(value)
    except ValueError:
        pass
    return value


@stringfilter
@register.filter
def replace(value, arg):
    args = arg.split()
    if len(args) != 2:
        return value
    return value.replace(args[0], args[1])
