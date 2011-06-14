from django import forms
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from ...forms import ConfirmationFormBase
from .models import SecurePayReceipt
from . import settings


class SecurePayConfirmationForm(ConfirmationFormBase):
    def __init__(self, *args, **kwargs):
        kwargs["action"] = settings.URL
        super(SecurePayConfirmationForm, self).__init__(self, *args, **kwargs)

        # Create a hidden field of each of the Secure Pay backend settings.
        # This means turning a setting like FORM_TABLE_BORDER into a hidden
        # field "table_border".
        for setting, value in settings:
            if not setting.starts_with("FORM_"):
                continue
            if value is not None:
                # turn FORM_TABLE_BORDER into table_border
                short = setting[5:].lower()
                field = forms.CharField(initial=value, widget=forms.HiddenInput())
                self.fields.insert(0, short, field)

        # Add the order items
        for item in self.payment.items:
            # Item is in form {"name": ..., "unit_price": ..., "quantity": ...}
            if item["name"] in self.fields:
                raise ValueError(u"Item name '%s' is not allowed as it clashes"
                                 u" with an existing field." % key)
            self.add_hidden_field(item["name"], "%s,%s" % (item["quantity"],
                                                           item["unit_price"]))

        # Add the customer's information
        # Secure Pay supports any number of customer information fields, so we
        # just include everything that is returned from signal handlers.
        data = self.payment.customer_data
        for key, value in data.iteritems():
            if key in self.fields:
                raise ValueError(u"Field '%s' is not allowed as part of "
                                 u"customer data." % key)
            self.add_hidden_field(key, value)
        self.add_hidden_field("information_fields", u",".join(data.keys()))

        # Set the return URL:
        if "return_link_url" not in self.fields:
            url = 'http://%s%s' % (
                Site.objects.get_current().domain,
                reverse('payme:securepay:conclusion', args=[self.payment.id]))
            self.add_hidden_field("return_link_url", url)

        # Set the callback URL:
        if "callback_url" not in self.fields:
            url = 'http://%s%s' % (
                Site.objects.get_current().domain,
                reverse('payme:securepay:callback', args=[self.payment.id]))
            self.add_hidden_field("callback_url", url)


    def __init__(self, *args, **kwargs):
        super(PaypalConfirmationForm, self).__init__(*args, **kwargs)
        w
        e
        e
        # We need a field called "return", but "return" is a keyword, so it has
        # to be defined here.
        r
        t
        y
        self.fields['return'] = forms.CharField(widget=forms.HiddenInput())
        paypal = get_backend_settings('paypal')
        customer = self.payment.get_customer_data()
        self.fields['invoice'].initial = self.payment.pk
        self.fields['first_name'].initial = customer.get('first_name', '')
        self.fields['last_name'].initial = customer.get('last_name', '')
        self.fields['email'].initial = customer.get('email', '')
        self.fields['city'].initial = customer.get('city', '')
        self.fields['country'].initial = customer.get('country_iso', '')
        self.fields['zip'].initial = customer.get('postal_code', '')
        self.fields['amount'].initial = self.payment.amount
        self.fields['currency_code'].initial = self.payment.currency
        self.fields['return'].initial = paypal['url']
        self.fields['business'].initial = paypal['email']
        i = 1
        for item in self.payment.get_items():
            self.fields['item_name_%d' % i] = forms.CharField(widget=forms.HiddenInput())
            self.fields['item_name_%d' % i].initial = item['name']
            self.fields['amount_%d' % i] = forms.DecimalField(widget=forms.HiddenInput())
            self.fields['amount_%d' % i].initial = item['unit_price']
            self.fields['quantity_%d' % i] = forms.DecimalField(widget=forms.HiddenInput())
            self.fields['quantity_%d' % i].initial = item['quantity']
            i += 1
        try:
            self.fields['return'].initial = paypal['return_url']
        except KeyError:
            # TODO: use https when needed
            self.fields['return'].initial = 'http://%s%s' % (
                    Site.objects.get_current().domain,
                    reverse('payme-paypal-return', kwargs={'payment_id': self.payment.id})
                    )
        self.fields['notify_url'].initial = 'http://%s%s' % (
                Site.objects.get_current().domain,
                reverse('payme-paypal-ipn')
                )

    def clean(self, *args, **kwargs):
        raise NotImplementedError("This form is not intended to be validated here.")
