from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.output_publish, name='output_publish'),
    # url(r'^tag/(?P<tag>.+)$', views.output_tags, name='output_tags'),
    url(r'^playlist/id(?P<id>\d+)$', views.output_playlist, name='output_playlist'),
    url(r'^post/id(?P<id>\d+)$', views.output_single_pubish, name='out_single_post'),
    # url(r'^product/(\d+)$', views.single_products, name='single_products'),
    # url(r'^developer/id([1-9])$', views.single_developer, name='single_developer'),
]