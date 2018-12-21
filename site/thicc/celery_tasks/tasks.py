from __future__ import absolute_import, unicode_literals
# from celery import current_app
from celery.contrib import rdb
from celery import Celery, shared_task
# current_app.conf.CELERY_ALWAYS_EAGER = True
# current_app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
from django.conf import settings
from .celery_app import app
from django.db.models import Count
from django.core.mail import send_mail
from game_info.models import Server
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.contrib.auth import get_user_model


#from twilio.rest import Client
#client = Client()

#@app.on_after_configure.connect
#def setup_periodic_tasks(sender, **kwargs):
#    # Calls test('world') every 30 seconds
#    sender.add_periodic_task(30.0, update_game_server_info.s(), expires=25, name='add every 10')

@app.task(ignore_result=True)
def update_game_server_info():
    for server in Server.objects.all():
        if server.get_info:
            server.update_info()
        if server.get_players:
            server.update_players()
        if server.get_rules:
            server.update_rules()


@app.task(ignore_result=True)
def send_email(subject, text_content, html_content, from_email, to):
    user = get_user_model().objects.get(email=to)
    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except BadHeaderError:
        user.forum_profile.email_unsubscribed = True
        user.forum_profile.save()

