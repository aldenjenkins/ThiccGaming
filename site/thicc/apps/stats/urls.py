from django.conf.urls import url
from . import views as stats_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', stats_views.StatsListView.as_view(), name='index'),
    # url(r'^search/$', stats_views.search, name='stat-search'),
    # url(r'^modify/(?P<sid>[0-9]+)/$', stats_views.modify, name='stat-modify'),
    #url(r'^add/$', login_required(stats_views.add), name='create'),
    # url(r'^comment/(?P<bid>[0-9]+)/$', stats_views.comment, name='comment'),
    #  url(r'^reban/(?P<bid>[0-9]+)/$', stats_views.reban, name= 'reban'),
    # url(r'^$', BanView.as_view(), name='bans'),
    # url(r'^contact/', views.contact, name = 'contact'),
]
