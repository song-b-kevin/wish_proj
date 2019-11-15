from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user/register$', views.register),
    url(r'^user/login$', views.login),
    url(r'^user/logout$', views.logout),
    url(r'^wishes$', views.wish_list),
    url(r'^wishes/stats$', views.wish_stats),
    url(r'^wishes/new$', views.wish_new),
    url(r'^wishes/create$', views.wish_create),
    url(r'^wishes/edit/(?P<wish_id>\d+)$', views.wish_edit_page),
    url(r'^wishes/edit', views.wish_edit_db),
    url(r'^wishes/(?P<wish_id>\d+)/remove$', views.wish_remove),
    url(r'^wishes/(?P<wish_id>\d+)/grant$', views.wish_grant),
    url(r'^wishes/(?P<wish_id>\d+)/like$', views.wish_like),
    url(r'^wishes/(?P<wish_id>\d+)/unlike$', views.wish_unlike),
]