from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^id(?P<id>\d+)$', views.out_profile_user, name='profile_user'),
    url(r'^id(?P<id>\d+)/edit$', views.edit_profile_user, name='edit_profile_user'),
    url(r'^id(?P<id>\d+)/edit/commit$', views.commit_edit_profile_user, name='commit_edit_profile_user'),
]