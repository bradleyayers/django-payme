from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module
from datetime import datetime
from .abstract_mixin import AbstractMixin
from . import signals
from . import settings


PAYMENT_STATUS_CHOICES = (
    ('new', _("New")),
    ('in_progress', _("In progress")),
    ('partially_paid', _("Partially paid")),
    ('paid', _("Paid")),
    ('failed', _("Failed")),
)


class PaymentFactory(models.Model, AbstractMixin):
    amount = models.DecimalField(decimal_places=4, max_digits=20)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='new')
    backend = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)
    paid_on = models.DateTimeField(blank=True, null=True, default=None)
    amount_paid = models.DecimalField(decimal_places=4, max_digits=20, default=0)

    class Meta:
        abstract = True

    @property
    def processor(self):
        try:
            backend = import_module(self.backend, package="mamona.backends")
            return backend.processor
        except (ImportError, AttributeError):
            raise ValueError("Backend '%s' is not available or provides no "
                             "processor." % self.backend)

    def change_status(self, new_status):
        """Always change payment's status via this method. Otherwise the signal
        will not be emitted."""
        old_status = self.status
        self.status = new_status
        self.save()
        signals.payment_status_changed.send(sender=type(self), instance=self,
                                            old_status=old_status, new_status=new_status)

    def on_payment(self, amount=None):
        """
        Launched by backend when payment receives any new money. It defaults to
        complete payment, but can optionally accept received amount as a
        parameter to handle partial payments.
        """
        self.paid_on = datetime.now()
        if amount:
            self.amount_paid = amount
        else:
            self.amount_paid = self.amount
        fully_paid = self.amount_paid >= self.amount
        if fully_paid:
            self.change_status('paid')
        else:
            self.change_status('partially_paid')
        urls = {}
        signals.return_urls_query.send(sender=type(self), instance=self, urls=urls)
        if not fully_paid:
            try:
                # Applications do NOT have to define 'partially_paid' URL.
                return urls['partially_paid']
            except KeyError:
                pass
        return urls['paid']

    def on_failure(self):
        "Launched by backend when payment fails."
        self.change_status('failed')
        urls = {}
        signals.return_urls_query.send(sender=type(self), instance=self, urls=urls)
        return urls['failure']

    @property
    def items(self):
        """
        Retrieves item list using signal query. Listeners must fill
        'items' list with at least one item. Each item is expected to be
        a dictionary, containing at least 'name' element and optionally
        'unit_price' and 'quantity' elements. If not present, 'unit_price'
        and 'quantity' default to 0 and 1 respectively.

        Listener is responsible for providing item list with sum of prices
        consistient with Payment.amount. Otherwise the final amount may
        differ and lead to unpredictable results, depending on the backend used.
        """
        default = {"unit_price": 0, "quantity": 1}
        items = []
        signals.order_items_query.send(sender=type(self), instance=self, items=items)
        if len(items) == 1:
            items[0].setdefault('unit_price', self.amount)
        for item in items:
            # update the item with the default values from *default*
            for key, value in default.iteritems():
                item.setdefault(key, value)
            assert item.has_key('name')
        return items

    @property
    def customer_data(self):
        """
        Retrieves customer data. The default empty dictionary is already the
        minimal implementation.
        """
        customer = {}
        signals.customer_query.send(sender=self.__class__, instance=self,
                                    customer=customer)
        return customer

    @classmethod
    def contribute(cls, order, **kwargs):
        return {'order': models.ForeignKey(order, **kwargs)}

    def __unicode__(self):
        return u"%s payment of %s%s%s for %s" % (
            self.get_status_display(),
            self.amount,
            self.currency,
            u" on %s" % self.paid_on if self.status == "paid" else "",
            self.order
        )


from django.db.models.loading import cache as app_cache
from .utils import import_backend_modules
def build_payment_model(order_class, **kwargs):
    class Payment(PaymentFactory.construct(order=order_class, **kwargs)):
        pass
    for backend in settings.BACKENDS.keys():
        models = import_module("mamona.backends.%s.models" % backend)
        app_cache.register_models("mamona", *models.build_models(Payment))
    return Payment


#def payment_from_order(order):
#    """Builds payment based on given Order instance."""
#    payment = Payment()
#    signals.payment_query.send(sender=None, order=order, payment=payment)
#    return payment
