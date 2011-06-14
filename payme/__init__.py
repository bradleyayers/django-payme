from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns("",
    url("^payment/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/$", "payme.views.detail", name="detail"),
    url("^payment/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/prepare/$", "payme.views.prepare", name="prepare"),
    url("^payment/(?P<ct_pk>[^/]+)/(?P<obj_pk>[^/]+)/confirm/$", "payme.views.confirm", name="confirm"),
    # backends
    ("^dummy/", include("payme.backends.dummy.urls", namespace="dummy")),
    ("^paypal/", include("payme.backends.paypal.urls", namespace="paypal")),
    ("^directone/", include("payme.backends.directone.urls", namespace="directone")),
    ("^securepay/", include("payme.backends.securepay.urls", namespace="securepay")),
)


urls = (urlpatterns, "payme", "payme")
