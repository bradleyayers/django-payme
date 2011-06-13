from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns("",
    #url("^order/$", "views.process_order", name="mamona-process-order"),
    url("^payment/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/$", "mamona.views.detail", name="detail"),
    url("^payment/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/prepare/$", "mamona.views.prepare", name="prepare"),
    url("^payment/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/confirm/$", "mamona.views.confirm", name="confirm"),
    # backends
    ("^dummy/", include("mamona.backends.dummy.urls", namespace="dummy")),
    ("^paypal/", include("mamona.backends.paypal.urls", namespace="paypal")),
    ("^directone/", include("mamona.backends.directone.urls", namespace="directone")),
    ("^securepay/", include("mamona.backends.securepay.urls", namespace="securepay")),
)


urls = (urlpatterns, "mamona", "mamona")
