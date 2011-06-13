from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('mamona.backends.securepay.views',
    url(r'^bounce/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/$', 'bounce', name='bounce'),
    url(r'^reply/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/$', 'callback', name='reply'),
    url(r'^payment/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/$', 'callback', name='payment'),
    #url(r'^success/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/$', 'success', name='success'),
    #url(r'^failure/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/$', 'failure', name='failure'),
)
