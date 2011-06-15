from django.conf.urls.defaults import *

urlpatterns = patterns('payme.backends.paypal.views',
    url(r'^return/(?P<payment_id>[0-9]+)/$', 'return_from_gw', name='payme-paypal-return'),
    url(r'^ipn/$', 'ipn', name='payme-paypal-ipn'),
)
