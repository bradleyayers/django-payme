import urllib2
from urllib import urlencode
from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from . import settings


def bounce(request, ct_pk, obj_pk):
    ct = get_object_or_404(ContentType, pk=ct_pk)
    payment = get_object_or_404(ct.model_class(), pk=obj_pk)

    return redirect(urls[payment.status])


@csrf_exempt
def reply(request, ct_pk, obj_pk):
    """
    When a payment is processed by DirectOne, their server makes a callback
    request to notify the status of the payment.
    """
    ct = get_object_or_404(ContentType, pk=ct_pk)
    payment = get_object_or_404(ct.model_class(), pk=obj_pk)

    receipt = Receipt(payment=payment)
    form = ReceiptForm(request.GET, instance=receipt)
    if form.is_valid():
        form.save()
    return HttpResponse()
