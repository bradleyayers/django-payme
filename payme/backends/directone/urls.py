from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('payme.backends.directone.views',
    url(r'^reply/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/$', 'reply', name='reply'),
    url(r'^bounce/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/$', 'bounce', name='bounce'),
)
