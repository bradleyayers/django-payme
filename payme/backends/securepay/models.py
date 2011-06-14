#! -*- coding: utf-8 -*-
from django.db import models


class SecurePayReceipt(models.Model):
    bill_id = models.CharField(max_length=200)
    field2 = models.CharField(max_length=200)
    approved = models.BooleanField()
    response = models.CharField(max_length=3)
    response_text = models.CharField(max_length=40)
    txn_id = models.CharField(max_length=6)
    receipt = models.CharField(max_length=6)
    amount = models.CharField(max_length=30, help_text=u"…in cents")
    sett_date = models.CharField(max_length=8, help_text=u"The bank settlement date.")
    card_type = models.CharField(max_length=10, help_text=u"A textual description of the card type used to make the payment, e.g. “Visa”, “MasterCard”, etc.")
    masked_cardno = models.CharField(max_length=12, help_text=u"The card number as first six…last three characters, e.g. 444433…111")
    preauth_id = models.CharField(max_length=6, blank=True, help_text=u"Returned only for a transaction type of preauthorisation")
    card_holder_name = models.CharField(max_length=60, blank=True, help_text=u"The card holder name")

    class Meta:
        app_label = "payme"

    def __unicode__(self):
        return self.bill_id

    #def callback_querystring(self):
    #    """
    #    Return a suitable call-back querystring that will instruct Secure Pay
    #    to include relevant data in a callback.
    #
    #    Note: the returned value does not start with a "?"
    #    """
    #    names = (x.name for x in self._meta.fields)
    #    exclude = ["id", "payment"]
    #    return '&'.join(("%s=" % n for n in names if n not in exclude))
