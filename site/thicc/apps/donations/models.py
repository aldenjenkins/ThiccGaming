from django.db import models
from django.db.models.signals import post_save, post_delete
from .signals import post_expire
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
#from social.apps.django_app.default.models import UserSocialAuth
from social_django.models import UserSocialAuth
from djangobb_forum.models import Profile
from game_info.models import Server
from valve.source.rcon import RCON

# Used for creating/removing in-game admin for donators
from thicc.apps.bans.models import Admin as Ban_Admin
from thicc.apps.bans.models import Group as Ban_Group

from datetime import timedelta


class PremiumDonation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    end_time = models.DateTimeField()
    expired = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s expires at %s" % (self.user, self.end_time)


@receiver(post_expire)
def premium_post_expire(sender, instance, **kwargs):
    group = Group.objects.get(name=settings.PREMIUM_GROUP_NAME)
    instance.user.groups.remove(group)
    profile = Profile.objects.get(user=instance.user)

    # User is not an admin and is a normal donator
    if(profile.status == "Premium"):
        profile.status = "Member"
        try:
            donator_admin = Ban_Admin.objects.get(authid=UserSocialAuth.objects.get(user_id=instance.user_id).uid)
            donator_admin.delete()
        except Exception:
            pass
        # reload_admins()
    profile.save()


@receiver(post_save, sender=PremiumDonation)
def premium_post_save(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name=settings.PREMIUM_GROUP_NAME)
        instance.user.groups.add(group)
        profile = Profile.objects.get(user=instance.user)

        # User is not an admin and is a normal donator
        if(profile.status == "Member" or profile.status == ""):
            profile.status = "Premium"
            admin_premium_group = Ban_Group.objects.get(textual_name="Premium")
            donator_admin = Ban_Admin(
                aid=instance.user, 
                user=instance.user,
                authid=UserSocialAuth.objects.get(user_id=instance.user_id).uid,
                srv_group=admin_premium_group,
                srv_flags=admin_premium_group.flags,
                immunity=admin_premium_group.immunity)
            donator_admin.save()
            # reload_admins()
        profile.save()


@receiver(valid_ipn_received)
def add_premium(sender, **kwargs):
    """
        When PayPal IPN completes, add the users premium
        set an expiry time
    """
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        try:
            social_user = UserSocialAuth.objects.get(uid=ipn_obj.custom)
        except ObjectDoesNotExist:
            # Todo: do something here as something has gone wrong
            return

        # Check which amount of donation time the person bought
        for x in settings.DONATION_AMOUNTS:
            if x[0] == ipn_obj.mc_gross:

                # Author: alden jenkins #
                # Checks if a donation for the user already exists and updates the end time if true.
                try:
                    existing_donation = PremiumDonation.objects.get(user_id=social_user.user_id)
                except Exception:
                    existing_donation = False
                if existing_donation:

                    if existing_donation.end_time > timezone.now():
                        existing_donation.end_time = existing_donation.end_time + timedelta(days=x[1])
                    else:
                        existing_donation.end_time = timezone.now() + timedelta(days=x[1])

                    existing_donation.save()
                else:
                    end_time = timezone.now() + timedelta(days=x[1])
                    PremiumDonation(
                        user=social_user.user,
                        end_time=end_time
                    ).save()


def reload_admins():
    servers = Server.objects.all()
    for server in servers:
        with RCON((server.host, server.port), settings.RCON_PASSWORD) as rcon:
            print(rcon("sm_reloadadmins"))
