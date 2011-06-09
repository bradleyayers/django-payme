from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.dispatch import receiver
from mamona import signals


@receiver(signals.urls_query, weak=False)
def handler(sender, instance, urls, **kwargs):
    url = 'http://%s%s' % (
        Site.objects.get_current().domain,
        reverse('show-order', kwargs={'order_id': instance.order.id})
    )
    urls.update({'paid': url, 'failure': url})


@receiver(signals.items_query, weak=False)
def handler(sender, instance=None, items=None, **kwargs):
    for item in instance.order.item_set.all():
        items.append({'name': item.name, 'unit_price': item.price})


@receiver(signals.payment_query, weak=False)
def handler(sender, order, payment, **kwargs):
    payment.order = order
    payment.amount = order.total
    payment.currency = order.currency


@receiver(signals.payment_status_changed, weak=False)
def handler(sender, instance, old_status, new_status, **kwargs):
    if new_status == 'paid':
        instance.order.status = 's'
        instance.order.save()
    elif new_status == 'failed':
        instance.order.status = 'f'
        instance.order.save()
    elif new_status == 'partially_paid':
        instance.order.status = 'p'
        instance.order.save()
