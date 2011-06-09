import urllib2
from urllib import urlencode
from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from mamona.models import Payment
from mamona.signals import urls_query
from . import settings


def bounce(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    urls = {}
    urls_query.send(sender=None, instance=payment, urls=urls)
    return redirect(urls[payment.status])


@csrf_exempt
def callback(request, pk):
    """
    When a payment is processed by Secure Pay, their server makes a callback
    request to notify the status of my payment.
    """
    payment = get_object_or_404(Payment, pk=pk)

    # Create a model form suitable for the receipt
    from .models import Receipt
    class ReceiptForm(forms.ModelForm):
        class Meta:
            model = Receipt

    receipt = Receipt(payment=payment)
    form = ReceiptForm(request.GET, instance=receipt)
    if form.is_valid():
        form.save()
    return HttpResponse()
