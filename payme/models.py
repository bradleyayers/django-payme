from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from payme.backends.securepay.models import SecurePayReceipt
from payme.backends.directone.models import DirectOneReceipt
from payme.backends import ALL as ALL_BACKENDS
from payme import signals
from payme import settings


class PaymentBase(models.Model):
    NEW = "new"
    IN_PROGRESS = "in progress"
    PAID = "paid"
    FAILED = "failed"

    STATUSES = (
        (NEW, _("New")),
        (IN_PROGRESS, _("In progress")),
        (PAID, _("Paid")),
        (FAILED, _("Failed")),
    )
    amount = models.DecimalField(decimal_places=4, max_digits=20)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, choices=STATUSES, default='new')
    backend_class_path = models.CharField(
            max_length=100, blank=True,
            choices=((x.class_path, x.name) for x in ALL_BACKENDS))
    created_on = models.DateTimeField(auto_now_add=True)
    paid_on = models.DateTimeField(blank=True, null=True, default=None)

    # generic relation to receipt
    receipt_content_type = models.ForeignKey("contenttypes.ContentType",
                                             blank=True, null=True)
    receipt_object_id = models.PositiveIntegerField(blank=True, null=True)
    receipt = generic.GenericForeignKey('receipt_content_type',
                                        'receipt_object_id')

    class Meta:
        abstract = True
        unique_together = ("receipt_content_type", "receipt_object_id")

    def __unicode__(self):
        return u"%s payment of %s%s%s" % (
            self.get_status_display(),
            self.amount,
            self.currency,
            (u" on %s" % self.paid_on) if self.status == self.PAID else "",
        )

    @property
    def backend_class(self):
        try:
            path, _, obj_name = self.backend_class_path.rpartition('.')
            mod = import_module(path)
            return getattr(mod, obj_name)
        except (ImportError, AttributeError):
            raise ValueError("Backend '%s' is not available"
                             % self.backend_class_path)

    def create_form(self):
        """
        Convenience method that proxies to ``Backend.create_form()`` using the
        payment's backend.
        """
        return self.backend_class().create_form(payment=self)

    def save(self, *args, **kwargs):
        # Overridden to allow status_changed to be emitted
        if self.pk:
            old = self.__class__.objects.get(pk=self.pk)
            status_changed = old.status != self.status
        else:
            status_changed = False
        result = super(PaymentBase, self).save(*args, **kwargs)
        if status_changed:
            signals.payment_status_changed.send(
                    sender=self.__class__, instance=self, old_instance=old)
        return result

    def clean(self):
        paid = self.paid_on or self.status in (self.PAID, self.FAILED)
        if paid:
            # Fill in any missing values that we might have
            self.paid_on = self.paid_on or datetime.now()
            self.status = self.status or self.PAID
        if not self.backend_class_path and len(settings.BACKENDS) == 1:
            self.backend_class_path = settings.BACKENDS.keys()[0]

    @property
    def success_url(self):
        """
        If defined, the user will be redirect to it after a successful payment.
        """
        return None

    @property
    def failure_url(self):
        """
        If not None, the user will be redirected to this URL after a failed
        payment attempt.
        """
        return None

    @property
    def items(self):
        """
        List of ``payme.items.Item`` objects.
        """
        return []

    @property
    def customer_details(self):
        """
        dict of customer data, use SortedDict to preserve order.
        """
        return {}

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)
