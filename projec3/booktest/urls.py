from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^\d+$', views.number),
    url(r'^How was rong$', views.rong)
]