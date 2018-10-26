from django.conf.urls import url
# from . import views
from .views import ScapeView

urlpatterns = [
    # url(r'^$', views.index, name = 'index'),
    url(r'^$', ScapeView.as_view(), name='index'),
    # url(r'^contact/', views.contact, name = 'contact'),
]