from django.conf.urls import patterns, include, url
from eweb import views
urlpatterns = patterns('',
                       url(r'^$', views.homepage, name='homepage'),
                       #url(r'^/', views.user_login, name='user_login'),
                       )
