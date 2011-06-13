from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('mamona.backends.directone.views',
    url(r'^reply/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/$', 'reply', name='reply'),
    url(r'^bounce/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/$', 'bounce', name='bounce'),
    url(r'^payment/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/$', 'payment', name='payment'),
)
