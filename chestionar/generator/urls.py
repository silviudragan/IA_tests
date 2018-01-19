from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Test.as_view(), name='index'),
    url(r'^test/$', views.Test.as_view(), name='test')
]