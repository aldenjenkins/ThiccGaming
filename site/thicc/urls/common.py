from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.i18n import set_language

from mezzanine.core.views import direct_to_template
from mezzanine.blog.views import blog_post_list
from mezzanine.conf import settings

from django.contrib.auth.views import password_change
from thicc.apps.django_azelphurmotd.views import radio, staff
from django.conf.urls.static import static

from thicc.core import custom_social_pipelines as custom_social_views
from thicc.core.custom_views import unsubscribe, verify_email
from django_prometheus import exports

from django.contrib.auth.decorators import user_passes_test


admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = i18n_patterns(
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    url(r'^{}/'.format(settings.ADMIN_URL_SLUG), include(admin.site.urls)),
    #url(r'^prometheus/', include('django_prometheus.urls', namespace='prometheus')),
    #url(r'^metrics$', user_passes_test(lambda u: u.is_staff)(exports.ExportToDjangoView), name='prometheus-django-metrics'),
    url(r'^metrics$', exports.ExportToDjangoView, name='prometheus-django-metrics'),
    #url(r'^silk/', include('silk.urls', namespace='silk')),
    url(r'^game_info/', include('game_info.urls')),
    url(r'^donate/', include('thicc.apps.donations.urls')),
    # url(r'^forum/user/(?P<username>.*)/social/$', login_required(TemplateView.as_view(template_name='profile_social.html'))),
    url(r'^forum/', include('djangobb_forum.urls', namespace='djangobb')),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^faq/', include('thicc.apps.faq.urls')),
    # url(
    #     r'^accounts/password_change/',
    #     password_change,
    #     {'post_change_redirect': '/forum', 'template_name': 'accounts/password_change.html'},
    #     name='account_change_password'
    # ),
    url(r'^email/$', custom_social_views.require_email, name='require_email'),
    url('', include('social_django.urls')),
    #url('', include('social.apps.django_app.urls', namespace='social')),
    # Temp Ingame Pages
    url(r'^rules/ingame/tf2/$', TemplateView.as_view(template_name='ingame/tf2/rules.html')),
    url(r'^radio/ingame/tf2/$', radio),
    url(r'^servers/ingame/tf2/$', TemplateView.as_view(template_name='ingame/tf2/servers.html')),
    url(r'^staff/ingame/tf2/$', staff),
    url(r'^news/ingame/tf2/$', TemplateView.as_view(template_name='ingame/tf2/news.html')),
    url(r'^howtosurf/ingame/tf2/$', TemplateView.as_view(template_name='ingame/tf2/howtosurf.html')),
    # url(r'^chat/', TemplateView.as_view(template_name='ingame/tf2/howtosurf.html')),
    url(r'^l4d2/', include('thicc.apps.l4d2.urls')),
    url(r'^gmod/', include('thicc.apps.gmod.urls')),
    # url(r'^wow/', include('thicc.apps.wow.urls')),
    # url(r'^scape/', include('thicc.apps.scape.urls')),

    # url(r'^csgo/', include('thicc.apps.csgo.urls')),
    url(r'^bans/', include('thicc.apps.bans.urls',  namespace='bans')),
    url(r'^about/', include('thicc.apps.about.urls')),
    url(r'^copyright/', include('thicc.apps.copyright.urls')),
    url(r'^rules/', include('thicc.apps.rules.urls')),
    url(r'^stats/', include('thicc.apps.stats.urls', namespace='stats')),
    url(r'^unsubscribe/(?P<user_id>\d+)/(?P<token>.*)/$', unsubscribe, name="unsubscribe-email"),
    url(r'^verifyemail/(?P<user_id>\d+)/(?P<token>.*)/$', verify_email, name="verify-email"),

)

# silk urls https://github.com/jazzband/django-silk

# Django Prometheus https://github.com/korfuri/django-prometheus

if settings.USE_MODELTRANSLATION:
    urlpatterns += [
        url('^i18n/$', set_language, name='set_language'),
    ]

urlpatterns += [
    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.

    # HOMEPAGE AS STATIC TEMPLATE
    # ---------------------------
    # This pattern simply loads the index.html template. It isn't
    # commented out like the others, so it's the default. You only need
    # one homepage pattern, so if you use a different one, comment this
    # one out.

    # url("^$", direct_to_template, {"template": "index.html"}, name="home"),

    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
    # ---------------------------------------------
    # This pattern gives us a normal ``Page`` object, so that your
    # homepage can be managed via the page tree in the admin. If you
    # use this pattern, you'll need to create a page in the page tree,
    # and specify its URL (in the Meta Data section) as "/", which
    # is the value used below in the ``{"slug": "/"}`` part.
    # Also note that the normal rule of adding a custom
    # template per page with the template name using the page's slug
    # doesn't apply here, since we can't have a template called
    # "/.html" - so for this case, the template "pages/index.html"
    # should be used if you want to customize the homepage's template.
    # NOTE: Don't forget to import the view function too!

    # url("^$", mezzanine.pages.views.page, {"slug": "/"}, name="home"),

    # HOMEPAGE FOR A BLOG-ONLY SITE
    # -----------------------------
    # This pattern points the homepage to the blog post listing page,
    # and is useful for sites that are primarily blogs. If you use this
    # pattern, you'll also need to set BLOG_SLUG = "" in your
    # ``settings.py`` module, and delete the blog page object from the
    # page tree in the admin if it was installed.
    # NOTE: Don't forget to import the view function too!

    url("^$", blog_post_list, name="home"),

    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!

    # If you'd like more granular control over the patterns in
    # ``mezzanine.urls``, go right ahead and take the parts you want
    # from it, and use them directly below instead of using
    # ``mezzanine.urls``.
    url("^", include("mezzanine.urls")),

    # MOUNTING MEZZANINE UNDER A PREFIX
    # ---------------------------------
    # You can also mount all of Mezzanine's urlpatterns under a
    # URL prefix if desired. When doing this, you need to define the
    # ``SITE_PREFIX`` setting, which will contain the prefix. Eg:
    # SITE_PREFIX = "my/site/prefix"
    # For convenience, and to avoid repeating the prefix, use the
    # commented out pattern below (commenting out the one above of course)
    # which will make use of the ``SITE_PREFIX`` setting. Make sure to
    # add the import ``from django.conf import settings`` to the top
    # of this file as well.
    # Note that for any of the various homepage patterns above, you'll
    # need to use the ``SITE_PREFIX`` setting as well.

    # ("^%s/" % settings.SITE_PREFIX, include("mezzanine.urls"))

]


# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.


    

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
#handler404 = "thicc.core.custom_views.page_not_found"
#handler500 = "thicc.core.custom_views.server_error"
