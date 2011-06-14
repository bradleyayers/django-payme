from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.dispatch import receiver
from payme.models import PaymentBase
from ..order.models import UnawareOrder
from payme import signals
from payme.items import Item


class Payment(PaymentBase):
    order = models.ForeignKey(UnawareOrder, related_name="payments")

    def full_clean(self, *args, **kwargs):
        self.amount = self.amount or self.order.total
        self.currency = self.currency or self.order.currency
        return super(PaymentBase, self).full_clean(*args, **kwargs)

    @property
    def success_url(self):
        return "http://%s%s" % (
                Site.objects.get_current().domain,
                reverse("show-order", kwargs={"order_id": self.order.id}))

    @property
    def failure_url(self):
        return self.success_url

    @property
    def items(self):
        return [Item(name=i.name, unit_price=i.price)
                for i in self.order.item_set.all()]


@receiver(signals.payment_status_changed, sender=Payment, weak=False)
def handler(sender, instance, **kwargs):
    if instance.status == Payment.PAID:
        instance.order.status = "s"
        instance.order.save()
    elif instance.status == Payment.FAILED:
        instance.order.status = "f"
        instance.order.save()
