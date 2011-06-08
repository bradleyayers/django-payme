from django import forms
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from ...forms import ConfirmationForm
from ...utils import get_backend_settings

from . import settings


class SecurePayConfirmationForm(ConfirmationForm):
    def __init__(self, *args, **kwargs):
        # Turn settings like FORM_TABLE_BORDER into hidden fields on the form.
        for setting in settings.__all__:
            if not setting.starts_with('FORM_'):
                continue
            value = getattr(settings, setting)
            if value is not None:
                # turn FORM_TABLE_BORDER into table_border
                name = setting[5:].lower()
                field = forms.CharField(initial=value, widget=forms.HiddenInput())
                self.fields.insert(0, name, field)


    def __init__(self, *args, **kwargs):
        super(PaypalConfirmationForm, self).__init__(*args, **kwargs)
        # We need a field called "return", but "return" is a keyword, so it has
        # to be defined here.
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
                    reverse('mamona-paypal-return', kwargs={'payment_id': self.payment.id})
                    )
        self.fields['notify_url'].initial = 'http://%s%s' % (
                Site.objects.get_current().domain,
                reverse('mamona-paypal-ipn')
                )

    def clean(self, *args, **kwargs):
        raise NotImplementedError("This form is not intended to be validated here.")
