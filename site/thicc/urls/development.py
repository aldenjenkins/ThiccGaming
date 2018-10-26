from django.conf.urls import url, include
from .common import urlpatterns as common_urlpatterns
#from rest_framework_swagger.views import get_swagger_view
import debug_toolbar
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    url(r'^__debug__/', include(debug_toolbar.urls)),
    # url(r'^silk/', include('silk.urls', namespace='silk')),
#    url(r'^docs/$', get_swagger_view(title='API Docs'), name='api_docs'),
) + common_urlpatterns

