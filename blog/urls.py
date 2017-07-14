from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.output_publish, name='output_publish'),
    url(r'^tag/(?P<tag>.+)$', views.output_tags, name='output_tags'),
    url(r'^playlist/id(?P<id>\d+)$', views.output_playlist, name='output_playlist'),
    url(r'^post/id(?P<id>\d+)$', views.output_single_pubish, name='out_single_post'),
    url(r'^ajax/post/id(?P<id>\d+)$', views.add_ajax),
    url(r"^comment/add_comment/(?P<post_id>\d+)$", views.add_comment, name='add_comment'),
    # url(r'^product/(\d+)$', views.single_products, name='single_products'),
    # url(r'^developer/id([1-9])$', views.single_developer, name='single_developer'),
]