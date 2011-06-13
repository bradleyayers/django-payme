from django.conf.urls.defaults import *
import mamona


urlpatterns = patterns('',
    url(r'^mamona/', include(mamona.urls)),
    url(r'^$', 'example.sales.views.order_singleitem', name='sales-order-singleitem'),
    url(r'^multiitem$', 'example.sales.views.order_multiitem', name='sales-order-multiitem'),
    url(r'^singlescreen$', 'example.sales.views.order_singlescreen', name='sales-order-singlescreen'),
    url(r'^details/(?P<order_id>[0-9]+)/$', 'example.order.views.show_order', name='show-order'),
)
