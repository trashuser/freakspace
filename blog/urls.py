from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.output_publish, name='output_publish'),
    # url(r'^product/(\d+)$', views.single_products, name='single_products'),
    # url(r'^developer/id([1-9])$', views.single_developer, name='single_developer'),
]