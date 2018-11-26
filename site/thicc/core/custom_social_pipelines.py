from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _
from social_django.utils import psa, load_strategy
from django.shortcuts import render
from social_core.pipeline.partial import partial
from social_core.backends.utils import load_backends
from social_core.backends.steam import SteamOpenId
from social_core.exceptions import AuthForbidden
from djangobb_forum.models import Profile, PostTracking
from functools import wraps
from mezzanine.accounts.forms import linear_search
from thicc.apps.stats.models import UserStats


def is_authenticated(user):
    if callable(user.is_authenticated):
        return user.is_authenticated()
    else:
        return user.is_authenticated


def associations(user, strategy):
    user_associations = strategy.storage.user.get_social_auth_for_user(user)
    if hasattr(user_associations, 'all'):
        user_associations = user_associations.all()
    return list(user_associations)


def common_context(authentication_backends, strategy, user=None, plus_id=None, **extra):
    """Common view context"""
    context = {
        'user': user,
        'available_backends': load_backends(authentication_backends),
        'associated': {}
    }

    if user and is_authenticated(user):
        context['associated'] = dict((association.provider, association)
                                     for association in associations(user, strategy))

    if plus_id:
        context['steam_key'] = plus_id
        context['steam_scope'] = ' '.join(SteamOpenId.DEFAULT_SCOPE)

    return dict(context, **extra)


def render_to(template):
    """Simple render_to decorator"""
    def decorator(func):
        """Decorator"""
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            """Rendering method"""
            out = func(request, *args, **kwargs) or {}
            if isinstance(out, dict):
                out = render(request, template, common_context(
                    settings.AUTHENTICATION_BACKENDS,
                    load_strategy(),
                    request.user,
                    steam_key=getattr(settings, 'SOCIAL_AUTH_STEAM_API_KEY', None),
                    **out
                ))
            return out
        return wrapper
    return decorator


@render_to('core/email_required.html')
def require_email(request):
    """Email required page"""
    strategy = load_strategy()
    partial_token = request.GET.get('partial_token')
    partial = strategy.partial_load(partial_token)
    return {
        'email_required': True,
        'partial_backend_name': partial.backend,
        'partial_token': partial_token
    }


def not_allowed_to_disconnect(strategy, details, user=None, is_new=False, *args, **kwargs):
    return False


@partial
def require_email_pipeline(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            current_partial = kwargs.get('current_partial')
            return strategy.redirect(
                '/email?partial_token={0}'.format(current_partial.token)
            )


def dont_allow_authenticated_pipeline(backend, strategy, details, user=None, is_new=False, request=None, *args, **kwargs):
    if is_authenticated(request.user): 
        messages.error(request, 
                       _("You cannot link Steam accounts to already \
                       existing accounts. You should have never even \
                       gotten this notification in the first place"))

        return strategy.redirect("/forum")


def check_email_pipeline(backend, strategy, details, user=None, is_new=False, request=None, *args, **kwargs):
    if is_new:
        if linear_search(details['email'].split('@')[-1]):
            messages.error(request, _("This email cannot be used. Please try again."))
            return strategy.redirect("/forum")
        if len(settings.AUTH_USER_MODEL.objects.filter(email=details['email'])) > 0:
            messages.error(request, _("This email is already associated with an account. Are you sure you are logging into the correct steam account?"))
            return strategy.redirect("/forum")


def get_steam_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    try:
        related_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        related_profile = Profile.objects.create(user=user)
        PostTracking.objects.create(user=user)
    avatar = details['player']['avatarfull']
    if avatar:
        related_profile.avatar = avatar
        related_profile.save()


def link_to_existing_stat_object(backend, strategy, details, response, user=None, social=None, is_new=False, request=None, *args, **kwargs):
    stats_object = UserStats.objects.filter(steam64=social.uid)[0]
    if stats_object:
        stats_object.linked_steam = social
        stats_object.save()
        if is_new:
            messages.info(strategy.request, _("We have all of your \
                                             stats from previous games you've played on our servers. Check them out!"))
    messages.success(strategy.request, _("Successfullly Logged In"))
