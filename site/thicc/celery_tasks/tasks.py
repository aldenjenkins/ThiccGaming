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


#from twilio.rest import Client
#client = Client()

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
def send_email(user_id, title, message):
    user = settings.AUTH_USER_MODEL.objects.get(pk=user_id)
    send_mail(user, title, message)

#@app.task(ignore_result=True)
#def send_notifications(user_id, message=None, sound=None, *args, **kwargs):
#    user = Account.objects.get(id=user_id)
#    ios_devices = user.my_apns_devices.filter(active=True)
#    android_devices = user.my_gcm_devices.filter(active=True)
#    if len(ios_devices) > 0 or len(android_devices) > 0:
#        badge_number = Notification.objects.filter(to_user=user, seen=False).count()
#        certfile = settings.PUSH_NOTIFICATIONS_SETTINGS['APNS_CERTIFICATE']
#        client = apns2_client.APNsClient(
#            certfile,
#            use_sandbox=False,
#            use_alternative_port=False
#        )
#        if sound == None:
#            data = [apns2_client.Notification(
#                        token=device.registration_id, payload=apns2_payload.Payload(badge_number, content_available=None, mutable_content=None, category=None,
#                        url_args=None, custom=None, thread_id=None)) for device in ios_devices]
#        else:
#            data = [apns2_client.Notification(
#                        token=device.registration_id, payload=apns2_payload.Payload(
#                        message, badge_number, sound, content_available=None, mutable_content=None, category=None,
#                        url_args=None, custom=None, thread_id=None)) for device in ios_devices]
#        client.connect()
#        data = client.send_notification_batch(
#                    data, topic=settings.PUSH_NOTIFICATIONS_SETTINGS['APNS_TOPIC'],
#                    priority=apns2_client.NotificationPriority.Immediate)
#        if message:
#            extra = {"sound":"default", "title":message.get('title',"")}
#            android_devices.send_message(message.get('body',None), extra=extra, **kwargs)
#
#
#@app.task(ignore_result=True)
#def send_bulk_notifications(user_ids, message=None, sound=None, *args, **kwargs):
#    users = Account.objects.filter(id__in=user_ids)
#    ios_devices = APNSDevice.objects.filter(active=True,user__in=users)
#    android_devices = GCMDevice.objects.filter(active=True, user__in=users)
#    if len(ios_devices) > 0 or len(android_devices) > 0:
#        # badge_numbers = Notification.objects.filter(to_user__in=users, seen=False).count()
#        certfile = settings.PUSH_NOTIFICATIONS_SETTINGS['APNS_CERTIFICATE']
#        client = apns2_client.APNsClient(
#            certfile,
#            use_sandbox=False,
#            use_alternative_port=False
#        )
#        if sound == None:
#            """ blank badge update """
#            data = \
#                [apns2_client.Notification(
#                    token=device.registration_id, payload=apns2_payload.Payload(Notification.objects.filter(to_user=device.user, seen=False).exclude(type="FriendsChangedNotification").count(), content_available=None, mutable_content=None, category=None,
#                    url_args=None, custom=None, thread_id=None)) for device in ios_devices]
#        else:
#            """ non-blank message """
#            data = \
#                [apns2_client.Notification(
#                    token=device.registration_id, payload=apns2_payload.Payload(
#                    message, Notification.objects.filter(to_user=device.user, seen=False).exclude(type="FriendsChangedNotification").count(), sound, content_available=None, mutable_content=None, category=None,
#                    url_args=None, custom=None, thread_id=None)) for device in ios_devices]
#        client.connect()
#        data = client.send_notification_batch(
#                    data, topic=settings.PUSH_NOTIFICATIONS_SETTINGS['APNS_TOPIC'],
#                    priority=apns2_client.NotificationPriority.Immediate)
#        if message:
#            extra = {"sound":"default", "title":message.get('title',"")}
#            android_devices.send_message(message.get('body',None), extra=extra, **kwargs)
#
#
#@app.task
#def recalc_local_post_hot(local_post_id):
#    local_post = LocalPost.objects.get(id=local_post_id)
#    local_post.hot = local_post.get_hot()
#    local_post.save()
#
#@app.task
#def recalc_local_comment_hot(local_comment_id):
#    local_comment = LocalComment.objects.get(id=local_comment_id)
#    local_comment.hot = local_comment.get_hot()
#    local_comment.save()
#
#@app.task
#def recalc_users_karma(user_id):
#    user = Account.objects.get(id=user_id)
#    karma = (
#        (user.my_referrals.count() * 5) +
#        user.my_upvotes.exclude(local_post__author=user).count() +
#        user.local_posts.filter(removed=False).aggregate(total=(Count('post_upvotes', distinct=True) - Count('post_downvotes', distinct=True) + Count('local_comments', distinct=True) + Count('id',distinct=True)))['total'] +
#        user.my_local_comments.filter(removed=False).aggregate(total=(Count('local_comment_upvotes', distinct=True) - Count('local_comment_downvotes', distinct=True) + Count('id', distinct=True)))['total'] +
#        user.users_metoo_posts.filter(removed=False).aggregate(total=(Count('attendees', distinct=True) + Count('id', distinct=True)))['total']
#    )
#    user.karma = karma
#    user.save()
#
#@app.task
#def send_email(email_address,subject,message):
#    send_mail(subject, message, 'hello@metoo.io', [email_address])
#
#@app.task
#def send_sms(to_number, from_number, message_body):
#    client.api.account.messages.create(
#        to=to_number,
#        from_=from_number,
#        body=message_body
#    )
#
#@app.task
#def like_bot(post_id):
#    try:
#        local_post = LocalPost.objects.get(id=post_id)
#    except LocalPost.DoesNotExist:
#        return
#    else:
#        local_post.random_upvote_check()
#
#
#@app.task
#def sendFriendMetoodAPlanNotification(plan_id, attendee_id, friend_id):
#   plan = MetooPost.objects.get(id=plan_id)
#   author = plan.author
#   attendee = Account.objects.get(id=attendee_id)
#   friend = Account.objects.get(id=friend_id)
#   if not Notification.objects.filter(
#       type='FriendMetoodAPlanNotification',
#       to_user=friend,
#       related_account=attendee,
#       related_metoo_post=plan,
#   ).exists():
#       if not Notification.objects.filter(
#           type='FriendMetoodAPlanNotification',
#           to_user=friend,
#           created_at__range=(datetime.datetime.now()-datetime.timedelta(days=1), datetime.datetime.now())
#       ).count() < 3:
#           Notification.objects.create(
#               type='FriendMetoodAPlanNotification',
#               to_user=friend,
#               related_account=attendee,
#               related_metoo_post=plan,
#           )
#           has_location = plan.location if plan.location else False
#           if has_location:
#               message = "Your friend %s metoo'd %s's plan at %s" % (attendee, author, plan.location)
#           else:
#               message = "Your friend %s metoo'd %s's plan: %s" % (attendee, author, plan.content)
#           send_notifications.delay(friend.id, {"body":message}, sound="default")
#
#
#
