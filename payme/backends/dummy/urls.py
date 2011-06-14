from django.conf.urls.defaults import *

urlpatterns = patterns('payme.backends.dummy.views',
    url(r'^decide/(?P<payment_id>[0-9]+)/$', 'decide_success_or_failure', name='payme-dummy-decide'),
    url(r'^success/(?P<payment_id>[0-9]+)/$', 'do_payment_success', name='payme-dummy-do-success'),
    url(r'^failure/(?P<payment_id>[0-9]+)/$', 'do_payment_failure', name='payme-dummy-do-failure'),
)
