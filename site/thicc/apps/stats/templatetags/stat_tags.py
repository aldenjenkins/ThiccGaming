from django import template
from djangobb_forum import settings as forum_settings
import hashlib
from django.utils.six.moves.urllib.parse import urlencode
import math
from datetime import datetime, timedelta
from django.utils.timesince import timesince


register = template.Library()


@register.simple_tag(takes_context=True)
def gravatar(context, email):
    if forum_settings.GRAVATAR_SUPPORT:
        if 'request' in context:
            is_secure = context['request'].is_secure()
        else:
            is_secure = False
        size = max(forum_settings.AVATAR_WIDTH, forum_settings.AVATAR_HEIGHT)
        url = 'https://secure.gravatar.com/avatar/%s?' if is_secure \
            else 'http://www.gravatar.com/avatar/%s?'
        url = url % hashlib.md5(email.lower().encode('ascii')).hexdigest()
        url += urlencode({
            'size': size,
            'default': forum_settings.GRAVATAR_DEFAULT,
        })
        return url.replace('&', '&amp;')
    else:
        return ''


@register.simple_tag(takes_context=True)
def minutes_to_duration(context, minutes):
    if minutes != '':
        #seconds  = math.floor((new Date() - date)/1000),
        interval = math.floor(int(minutes) / 525600)
        #  console.log("seconds: " + seconds + " interval: " + interval)
        if interval >= 1:
            return str(interval) + " years"
        interval = math.floor(minutes / 42800)
        if interval >= 1:
            return str(interval) + " months"
        interval = math.floor(minutes / 1440)
        if interval >= 1:
            return str(interval) + " days"
        interval = math.floor(minutes / 60)
        if interval >= 1:
            return str(interval) + " hours"
        return str(math.floor(minutes)) + " minutes"
    return ''


@register.simple_tag(takes_context=True)
def age_from_char_epoch(context, value):
    if value != '':
        now = datetime.now()
        value = datetime.fromtimestamp(int(value))
        try:
            difference = now - value
        except Exception:
            return value

        if difference <= timedelta(minutes=1):
            return 'just now'
        return '%(time)s ago' % {'time': timesince(value)}  # .split(', ')[0]}
    return ''
