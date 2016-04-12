from django.conf.urls import patterns, include, url
from eweb import views
urlpatterns = patterns('',
                       url(r'^$', views.homepage, name='homepage'),
                       url(r'^login', views.login, name='login'),
                       url(r'^register', views.register, name='register'),
                       url(r'^cart/$', views.cart, name='cart'),
                       url(r'^good/(?P<product_id>[\d]+)',
                           views.goodsinfo, name='goodsinfo'),

                       url(r'^order/$', views.order, name='order'),
                       )
