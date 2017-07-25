from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.output_publish, name='output_publish'),
    url(r'^tag/(?P<tag>.+)$', views.output_tags, name='output_tags'),

    url(r'^playlist/id(?P<id>\d+)$', views.output_playlist, name='output_playlist'),
    url(r'^playlist/create/$', views.create_playlist, name='create_playlist'),
    url(r'^playlist/create/add/$', views.commit_playlist, name='commit_playlist'),
    url(r'^playlist/id(?P<id_playlist>\d+)/edit/$', views.create_playlist, name='edit_playlist'),
    url(r'^playlist/id(?P<id_playlist>\d+)/edit/commit$', views.commit_playlist_edit, name='commit_edit_playlist'),

    url(r'^post/write/$', views.write_post, name='write_post'),
    url(r'^post/write/add/$', views.add_post, name='add_post'),
    url(r'^post/id(?P<id>\d+)$', views.output_single_pubish, name='out_single_post'),
    url(r'^post/id(?P<id_post>\d+)/edit/$', views.write_post, name='edit_post'),
    url(r'^post/id(?P<id_post>\d+)/commit/$', views.commit_post, name='edit_post_commit'),

    url(r'^ajax/post/id(?P<id>\d+)$', views.add_ajax),
    url(r"^comment/add_comment/(?P<post_id>\d+)$", views.add_comment, name='add_comment'),
]
