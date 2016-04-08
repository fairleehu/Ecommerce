from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'ecom.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^eweb/', include('eweb.urls')),
                       )
from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^res/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
