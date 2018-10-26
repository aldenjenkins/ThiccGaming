from django.conf.urls import url
from . import views as ban_views
from django.contrib.auth.decorators import login_required
# from .views import BanView

urlpatterns = [
    url(r'^$', ban_views.index, name = 'index'),
    url(r'^search/$', ban_views.search, name = 'search'),
    url(r'^unban/(?P<bid>[0-9]+)/$', ban_views.unban, name = 'unban'),
    url(r'^ban/$', login_required(ban_views.ban), name= 'ban'),
    url(r'^comment/(?P<bid>[0-9]+)/$', ban_views.comment, name= 'comment'),
    url(r'^reban/(?P<bid>[0-9]+)/$', ban_views.reban, name= 'reban'),
    # url(r'^$', BanView.as_view(), name='bans'),
    # url(r'^contact/', views.contact, name = 'contact'),
]