from urllib import urlencode
from django import forms
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from ...forms import ConfirmationFormBase
from .models import DirectOneReceipt
from . import settings


def get_reply_querystring(payment):
    names = (x.name for x in payment._meta.fields)
    exclude = ["id", "payment"]
    return urlencode(dict(((n, "") for n in names if n not in exclude)))


class DirectOneReceiptForm(forms.ModelForm):
    class Meta:
        model = DirectOneReceipt


class DirectOneConfirmationForm(ConfirmationFormBase):
    def __init__(self, *args, **kwargs):
        kwargs["action"] = settings.URL
        super(DirectOneConfirmationForm, self).__init__(*args, **kwargs)

        # Create a hidden field of each of the Secure Pay backend settings.
        # This means turning a setting like FORM_TABLE_BORDER into a hidden
        # field "table_border".
        for setting, value in settings.iterall():
            if not setting.startswith("FORM_"):
                continue
            if value is not None:
                # turn FORM_TABLE_BORDER into table_border
                short = setting[5:].lower()
                field = forms.CharField(initial=value, widget=forms.HiddenInput())
                self.fields.insert(0, short, field)

        # Add the order items
        for item in self.payment.items:
            # Item is in form {"name": ..., "unit_price": ..., "quantity": ...}
            if item.name in self.fields:
                raise ValueError(u"Item name '%s' is not allowed as it clashes"
                                 u" with an existing field." % key)
            self.add_hidden_field(item.name,
                                  "%s,%s" % (item.quantity, item.unit_price))

        # Add the customer's information
        # Secure Pay supports any number of customer information fields, so we
        # just include everything that is returned from signal handlers.
        data = self.payment.customer_details
        for key, value in data.iteritems():
            if key in self.fields:
                raise ValueError(u"Field '%s' is not allowed as part of "
                                 u"customer data." % key)
            self.add_hidden_field(key, value)
        self.add_hidden_field("information_fields", u",".join(data.keys()))

        ct = ContentType.objects.get_for_model(self.payment)

        # Set the return URL:
        if "return_link_url" not in self.fields:
            url = "http://%s%s" % (
                Site.objects.get_current().domain,
                reverse("payme:directone:bounce", kwargs={
                    "ct_pk": ct.pk, "obj_pk": self.payment.pk}))
            self.add_hidden_field("return_link_url", url)

        # The *reply_link_url* is a URL that DirectOne makes a callback to
        # before redirecting the user back.
        if "reply_link_url" not in self.fields:
            path = reverse("payme:directone:reply",
                           kwargs={"ct_pk": ct.pk, "obj_pk": self.payment.pk})
            querystring = get_reply_querystring(self.payment)
            url = "http://%s%s?%s" % (Site.objects.get_current().domain,
                                      path,
                                      querystring)
            self.add_hidden_field("reply_link_url", url)
