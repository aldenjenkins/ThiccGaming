
from __future__ import absolute_import, unicode_literals
import os
from django.utils.translation import ugettext_lazy as _


######################
# MEZZANINE SETTINGS #
######################

# The following settings are already defined with default values in
# the ``defaults.py`` module within each of Mezzanine's apps, but are
# common enough to be put here, commented out, for conveniently
# overriding. Please consult the settings documentation for a full list
# of settings Mezzanine implements:
# http://mezzanine.jupo.org/docs/configuration.html#default-settings

# Controls the ordering and grouping of the admin menu.
#
# ADMIN_MENU_ORDER = (
#     ("Content", ("pages.Page", "blog.BlogPost",
#        "generic.ThreadedComment", (_("Media Library"), "fb_browse"),)),
#     ("Site", ("sites.Site", "redirects.Redirect", "conf.Setting")),
#     ("Users", ("auth.User", "auth.Group",)),
# )

# A three item sequence, each containing a sequence of template tags
# used to render the admin dashboard.
#
# DASHBOARD_TAGS = (
#     ("blog_tags.quick_blog", "mezzanine_tags.app_list"),
#     ("comment_tags.recent_comments",),
#     ("mezzanine_tags.recent_actions",),
# )

TIME_ZONE = 'America/New_York'

# A sequence of templates used by the ``page_menu`` template tag. Each
# item in the sequence is a three item sequence, containing a unique ID
# for the template, a label for the template, and the template path.
# These templates are then available for selection when editing which
# menus a page should appear in. Note that if a menu template is used
# that doesn't appear in this setting, all pages will appear in it.

# PAGE_MENU_TEMPLATES = (
#     (1, _("Top navigation bar"), "pages/menus/dropdown.html"),
#     (2, _("Left-hand tree"), "pages/menus/tree.html"),
#     (3, _("Footer"), "pages/menus/footer.html"),
# )

# A sequence of fields that will be injected into Mezzanine's (or any
# library's) models. Each item in the sequence is a four item sequence.
# The first two items are the dotted path to the model and its field
# name to be added, and the dotted path to the field class to use for
# the field. The third and fourth items are a sequence of positional
# args and a dictionary of keyword args, to use when creating the
# field instance. When specifying the field class, the path
# ``django.models.db.`` can be omitted for regular Django model fields.
#
# EXTRA_MODEL_FIELDS = (
#     (
#         # Dotted path to field.
#         "mezzanine.blog.models.BlogPost.image",
#         # Dotted path to field class.
#         "somelib.fields.ImageField",
#         # Positional args for field class.
#         (_("Image"),),
#         # Keyword args for field class.
#         {"blank": True, "upload_to": "blog"},
#     ),
#     # Example of adding a field to *all* of Mezzanine's content types:
#     (
#         "mezzanine.pages.models.Page.another_field",
#         "IntegerField", # 'django.db.models.' is implied if path is omitted.
#         (_("Another name"),),
#         {"blank": True, "default": 1},
#     ),
# )

IS_PROD = True if os.getenv("IS_PRODUCTION") else False

DEBUG = os.getenv("DEBUG", False)

# URLCONF
if IS_PROD:
    ROOT_URLCONF = 'thicc.urls.common'
    ALLOWED_HOSTS = ['localhost','django', 'thicc.io', 'www.thicc.io', 'thiccgaming.com', 'www.thiccgaming.com']
elif DEBUG:
    #ROOT_URLCONF = 'thicc.urls.development'
    ROOT_URLCONF = 'thicc.urls.development'
    ALLOWED_HOSTS = ['django', 'localhost', '127.0.0.1']
else:
    ROOT_URLCONF = 'thicc.urls.common'
    ALLOWED_HOSTS = ['localhost','django', 'dev.thicc.io']

ADMIN_URL_SLUG = os.getenv("ADMIN_URL", 'admin')

# Setting to turn on featured images for blog posts. Defaults to False.
BLOG_USE_FEATURED_IMAGE = False

# If True, the django-modeltranslation will be added to the
# INSTALLED_APPS setting.
USE_MODELTRANSLATION = False

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

# Supported languages
LANGUAGES = (
    ('en', _('English')),
)

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = os.getenv("SITE_ID")

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

AUTHENTICATION_BACKENDS = (
    # "social.backends.steam.SteamOpenId",
    "social_core.backends.steam.SteamOpenId",
    # "social.backends.twitter.TwitterOAuth",
    # "social.backends.google.GoogleOAuth2",
    # "social.backends.github.GithubOAuth2",
    # "social.backends.facebook.FacebookOAuth2",
    # "social.backends.reddit.RedditOAuth2",
    # POTENTIALLY UN COMMENT THIS. THIS WAS COMMENTED AFTER THE THICC GAMING CHANGE AND RIGHT BEFORE MAKING AUTH EXCLUSIVELY STEAM OAUTH. NOT SURE OF SIDE EFFECTS.    
    "mezzanine.core.auth_backends.MezzanineBackend",
)

SOCIAL_AUTH_STEAM_API_KEY = os.getenv('STEAM_KEY')

SOCIAL_AUTH_PIPELINE = (
    'thicc.core.custom_social_pipelines.dont_allow_authenticated_pipeline',
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social_core.pipeline.social_auth.social_user',

    'thicc.core.custom_social_pipelines.require_email_pipeline',
    #'social_core.pipeline.debug.debug',
    'thicc.core.custom_social_pipelines.check_email_pipeline',
    #'social_core.pipeline.debug.debug',
    #'common.pipeline.require_country',
    #'common.pipeline.require_city',

    'social_core.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social_core.pipeline.mail.mail_validation',


    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'thicc.core.custom_social_pipelines.get_steam_avatar',
    'thicc.core.custom_social_pipelines.link_to_existing_stat_object',
    'thicc.core.custom_social_pipelines.send_welcome_mail',
    'thicc.core.custom_social_pipelines.send_private_message',
    #'thicc.core.custom_social_pipelines.save_profile',
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'thicc.core.custom_social_pipelines.not_allowed_to_disconnect',

    # Verifies that the social association can be disconnected from the current
    # user (ensure that the user login mechanism is not compromised by this
    # disconnection).
    #'social_core.pipeline.disconnect.allowed_to_disconnect',

    # Collects the social associations to disconnect.
    #'social_core.pipeline.disconnect.get_entries',

    # Revoke any access_token when possible.
    #'social_core.pipeline.disconnect.revoke_tokens',

    # Removes the social associations.
    #'social_core.pipeline.disconnect.disconnect',
)

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644


#############
# DATABASES #
#############

# DATABASES = {
#     "default": {
#         # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
#         "ENGINE": "django.db.backends.",
#         # DB name or path to database file if using sqlite3.
#         "NAME": "",
#         # Not used with sqlite3.
#         "USER": "",
#         # Not used with sqlite3.
#         "PASSWORD": "",
#         # Set to empty string for localhost. Not used with sqlite3.
#         "HOST": "",
#         # Set to empty string for default. Not used with sqlite3.
#         "PORT": "",
#     }
# }


RCON_PASSWORD = os.getenv('RCON_PASSWORD', '')

# APPEND_SLASH = False
#########
# PATHS #
#########

# Full filesystem path to the project.
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

#CACHES = {
#    'default': {
#        'BACKEND': 'django_prometheus.cache.backends.filebased.FileBasedCache',
#        'LOCATION': '/var/tmp/django_cache',
#    }
#}

CACHES = {
    'default': {
        #'BACKEND': 'redis_cache.RedisCache',
        'BACKEND': 'django_prometheus.cache.backends.redis.RedisCache',
        "LOCATION": "redis://redis:6379/1",
        #'LOCATION': [
        #    '%s:%s' % (os.getenv('PROD_REDIS_MASTER_SERVICE_HOST', '127.0.0.1'),
        #               os.getenv('PROD_REDIS_MASTER_SERVICE_PORT', 6379)),
        #    '%s:%s' % (os.getenv('PROD_REDIS_SLAVE_SERVICE_HOST', '127.0.0.1'),
        #               os.getenv('PROD_REDIS_SLAVE_SERVICE_PORT', 6379))
        #
        # ],
        'OPTIONS': {
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'PICKLE_VERSION': 2,
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        #    'MASTER_CACHE': '%s:%s' % (
        #        os.getenv('PROD_REDIS_MASTER_SERVICE_HOST', '127.0.0.1'),
        #        os.getenv('PROD_REDIS_MASTER_SERVICE_PORT', 6379))
        },
    },
}

AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_BUCKET")
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_KEY")
AWS_S3_FILE_OVERWRITE = False

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
DEFAULT_FILE_STORAGE = 'thicc.core.storage_backends.CustomS3Boto3Storage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# silence django-storages warning message
AWS_DEFAULT_ACL = "public-read"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

LOGOUT_REDIRECT_URL = "/forum"

################
# APPLICATIONS #
################

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.pages",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.galleries",
    "mezzanine.twitter",
    "mezzanine.accounts",
    # thicc.apps. "mezzanine.mobile",
    "game_info",
    "rest_framework",
    "djangobb_forum",
    #"social.apps.django_app.default",
    "social_django",
    "thicc.apps.donations",
    "paypal.standard.ipn",
    "nocaptcha_recaptcha",
    "thicc.apps.faq",
    "django_messages",
    "thicc.apps.social_auth_filter",
    #"thicc.apps.djangobb_to_irc",
    'thicc.apps.django_azelphurmotd',
    'thicc.apps.scape',
    'thicc.apps.bans',
    'thicc.apps.stats',
    'storages',
    'django_celery_beat',
    #'silk',
    #'django_prometheus',
)

apps = INSTALLED_APPS

DEBUG_APPS = (
    #'debug_toolbar',
    #'django_pdb',
)


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_ROOT, "templates")
        ],
        #"APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.static",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.tz",
                "mezzanine.conf.context_processors.settings",
                "mezzanine.pages.context_processors.page",
                #"social.apps.django_app.context_processors.backends",
                #"social.apps.django_app.context_processors.login_redirect",
                "social_django.context_processors.backends",
                "thicc.apps.donations.processors.donations",
                "game_info.processors.servers",
                "djangobb_forum.context_processors.forum_settings",
                "django_messages.processors.get_messages"
            ],
            "builtins": [
                "mezzanine.template.loader_tags",
            ],
            "loaders": [
                "mezzanine.template.loaders.host_themes.Loader",
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ]
        },
    },
]
    

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    "mezzanine.core.middleware.UpdateCacheMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'silk.middleware.SilkyMiddleware',
    # Uncomment if using internationalisation or localisation
    #'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    #"mezzanine.core.middleware.TemplateForDeviceMiddleware",
    #"mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
    "djangobb_forum.middleware.LastLoginMiddleware",
    'djangobb_forum.middleware.UsersOnline',
    'djangobb_forum.middleware.TimezoneMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]


DEBUG_MIDDLEWARE = [
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    #'thicc.core.custom_middleware.ProfilerMiddleware',
    #'django_pdb.middleware.PdbMiddleware',

]


def show_the_toolbar(request):
    return request.user.id == 1


#SILKY_PYTHON_PROFILER = True
#SILKY_AUTHENTICATION = True  # User must login
#SILKY_AUTHORISATION = True  # User must have permissions
#SILKY_PERMISSIONS = lambda user: user.is_superuser
#
#SILKY_META = True


if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + DEBUG_APPS
    MIDDLEWARE = MIDDLEWARE + DEBUG_MIDDLEWARE
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': 'thicc.settings.show_the_toolbar',
        # rest of config
    }
    INTERNAL_IPS = ('127.0.0.1',)
else:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_UNIQUE_URL',''),
        integrations=[DjangoIntegration()]
    )

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "django_extensions",
    "compressor",
    "coverage",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Haystack settings
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, 'djangobb_index')
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine'
    }
}


DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', 'dev.db'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_IP', ''),
        'PORT': os.getenv('DB_PORT', '')
    }
}

PAYPAL_RECEIVER_EMAIL = os.getenv('PAYPAL_EMAIL', '')
PAYPAL_TEST = False

DONATION_AMOUNTS = (
    # Amount, Days of premium
    (5, 30),
    (10, 90),
    (15, 180),
    (25, 365),
)

# Target donation amount for sidebar
MONTHLY_DONATION_AMOUNT = 100

PREMIUM_GROUP_NAME = "Premium"

ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = ("first_name", "last_name")

LOGIN_REDIRECT_URL = "/forum/"

BLOG_SLUG = 'news'

COMMENTS_ACCOUNT_REQUIRED = True
COMMENTS_DEFAULT_APPROVED = True

COMMENT_FORM_CLASS = "thicc.forms.MyCommentForm"

ACCOUNTS_PROFILE_FORM_CLASS = "thicc.forms.MyProfileForm"

DJANGOBB_AUTHORITY_SUPPORT = False
DJANGOBB_AVATAR_WIDTH = 80
DJANGOBB_AVATAR_HEIGHT = 80
DJANGOBB_FORUM_LOGO_WIDTH = 27
DJANGOBB_FORUM_LOGO_HEIGHT = 27
DJANGOBB_USER_TO_USER_EMAIL = False
DJANGOBB_PM_SUPPORT = True

DJANGOBB_ATTACHMENT_SIZE_LIMIT= 5000000

SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'

# ACCOUNTS_VERIFICATION_REQUIRED = True


# Directory in which upload streamed files will be temporarily saved. A value of
# `None` will make Django use the operating system's default temporary directory
# (i.e. "/tmp" on *nix systems).
FILE_UPLOAD_TEMP_DIR = MEDIA_ROOT + "temp/"


# The email backend to use. For possible shortcuts see django.core.mail.
# The default is to use the SMTP backend.
# Third-party backends can be specified by providing a Python path
# to a module that defines an EmailBackend class.
EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'
# Default email address to use for various automated correspondence from
# the site managers.
DEFAULT_FROM_EMAIL = os.getenv("MAIL_FROM")
PM_FROM_EMAIL = os.getenv("PM_MAIL_FROM")

OWNER_EMAIL = os.getenv("OWNER_EMAIL")

# Subject-line prefix for email messages send with django.core.mail.mail_admins
# or ...mail_managers.  Make sure to include the trailing space.
#EMAIL_SUBJECT_PREFIX = '[Django] '

AVATAR_ALLOWED_FILE_EXTS = (
                            ".png",
                            ".gif",
                            ".jpg",
                            ".jpeg",
)

# These variables will be overwritten by local settings, but aren't
# really required in a development environment. I'm nulling them here
# so that the development server will start without these variables
# being set
#
NORECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_KEY")
NORECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET")

RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

SECRET_KEY = os.getenv('SECRET_KEY')

DJANGOBB_ENABLE_POLLS = True

USE_TZ = True

##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.

# Instead of doing "from .local_settings import *", we use exec so that
# local_settings has full access to everything defined in this module.

#f = os.path.join(PROJECT_APP_PATH, "local_settings.py")
#if os.path.exists(f):
#    exec(open(f, "rb").read())


####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
