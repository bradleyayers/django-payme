from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from django.utils import simplejson
from . import settings
from .forms import DirectOneReceiptForm


def bounce(request, ct_pk, obj_pk):
    ct = get_object_or_404(ContentType, pk=ct_pk)
    payment = get_object_or_404(ct.model_class(), pk=obj_pk)
    if payment.status == payment.SUCCESS:
        url = payment.success_url or "payme:directone:payment"
    elif payment.status == payment.FAILED:
        url = payment.failed_url or "payme:directone:payment"
    else:
        url = "payme:directone:payment"
    return redirect(url)


@csrf_exempt
def reply(request, ct_pk, obj_pk):
    """
    When a payment is processed by DirectOne, their server makes a callback
    request to notify the status of the payment.
    """
    ct = get_object_or_404(ContentType, pk=ct_pk)
    payment = get_object_or_404(ct.model_class(), pk=obj_pk)
    form = DirectOneReceiptForm(request.GET)
    if form.is_valid():
        payment.receipt = form.save()
        payment.paid_on = datetime.now()
        payment.full_clean()
        payment.save()
        return HttpResponse("All good!")
    else:
        errors = {}
        for field, errorlist in form.errors.iteritems():
            errors[field] = [unicode(e) for e in errorlist]
        json = simplejson.dumps(errors)
        return HttpResponse(json, content_type="application/json",
                            status=400)
