from django import template
from datetime import timedelta
from django.utils import timezone
from django.utils.timesince import timesince, timeuntil

register = template.Library()


@register.simple_tag(takes_context=True)
def age_of(context, value):
    now = timezone.now()
    if now > value:
        return '%(time)s ago' % {'time': timesince(value)}
    else:
        return 'In %(time)s' % {'time': timeuntil(value)}  # .split(', ')[0]}
