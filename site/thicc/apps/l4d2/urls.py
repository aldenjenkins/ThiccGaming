from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^banner', views.banner, name = 'banner'),
    # url(r'^contact/', views.contact, name = 'contact'),
]