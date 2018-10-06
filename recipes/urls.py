from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url('^about/$', views.about, name='about'),
    url('^contact/$', views.contact, name='contact'),
    url('<slug:id>/$', views.detail, name='detail'),
    url(r'(?P<id>[\w\-]+)/$', views.detail, name='detail')
]
