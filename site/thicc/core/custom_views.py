from .custom_social_pipelines import get_token_for_user
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import requires_csrf_token
from django.template.loader import get_template
from django.contrib.auth import get_user_model


def unsubscribe(request, user_id, token, template='unsubscribe.html',
                extra_context=None):

    user = get_object_or_404(get_user_model(), pk=user_id)
    profile = user.forum_profile
    if profile.email_unsubscribed:
        messages.success(request, "You have SUCCessfully been unsubscribed to all thread updates.")
        #return render_to_response(template, context={'unsubbed_user': user})
        return redirect('/forum')

    the_token = get_token_for_user(user)
    if not token == the_token:
        #raise Http404
        raise Http500

    profile.email_verified = True
    profile.email_unsubscribed = True
    profile.save()
    
    messages.success(request, "You have SUCCessfully been unsubscribed to all thread updates.")

    #return render_to_response(template, context={'unsubbed_user': user})
    return redirect('/forum')


def verify_email(request, user_id, token,
                 extra_context=None):

    user = get_object_or_404(settings.AUTH_USER_MODEL, id=user_id)
    profile = user.forum_profile
    if profile.email_verified:
        messages.info(request, _("Email has already been verified."))
        #return render_to_response('already_verified_email.html', context={'verified_user': user})
        return redirect('/forum')

    the_token = get_token_for_user(user)
    if not token == the_token:
        raise Http404

    profile.email_verified = True
    profile.save()

    messages.info(request, _("Email SUCCessfully verified."))
    #return render_to_response(template, context={'verified_user': user})
    return redirect('/forum')
