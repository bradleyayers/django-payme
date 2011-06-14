from urllib import urlencode
from urlparse import urlunparse
from django.http import HttpResponseNotFound, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.contrib.contenttypes.models import ContentType
from .forms import PaymentBackendForm
from . import settings


def prepare(request, ct_pk, obj_pk):
    """
    Prompt the user for any final input for the payment, or redirect to the
    confirmation page.
    """
    ct = get_object_or_404(ContentType, pk=ct_pk)
    Payment = ct.model_class()  # Payment is some subclass of PaymentBase
    payment = get_object_or_404(Payment, pk=obj_pk, status=Payment.NEW)

    if request.method == "POST":
        form = PaymentBackendForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
    else:
        form = PaymentBackendForm(instance=payment)
    if payment.backend_class_path:
        return redirect("payme:confirm", ct_pk=ct_pk, obj_pk=obj_pk)
    else:
        return direct_to_template(
                request, "payme/select_payment_backend.html",
                {"payment": payment, "form": form})


def confirm(request, ct_pk, obj_pk):
    ct = get_object_or_404(ContentType, pk=ct_pk)
    Payment = ct.model_class()  # Payment is some subclass of PaymentBase
    payment = get_object_or_404(Payment, pk=obj_pk, status=Payment.NEW)
    form = payment.create_form()
    return direct_to_template(request, "payme/confirm.html",
                              {"form": form, "payment": payment})


def detail(request, ct_pk, obj_pk):
    ct = get_object_or_404(ContentType, pk=ct_pk)
    payment = get_object_or_404(ct.model_class(), pk=obj_pk)
    return HttpResponse("Payment: " + payment.status)
