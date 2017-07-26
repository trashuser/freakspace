from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^id(?P<id>\d+)$', views.out_profile_user, name='profile_user'),
]