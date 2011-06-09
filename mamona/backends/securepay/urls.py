from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('mamona.backends.securepay.views',
    url(r'^bounce/([^/]+)/$', 'bounce', name='manona-securepay-bounce'),
    url(r'^callback/([^/]+)/$', 'callback', name='manona-securepay-callback'),
)
