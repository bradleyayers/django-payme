from urllib import urlencode
from urlparse import urlunparse
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.contrib.contenttypes.models import ContentType
from .forms import PaymentMethodForm
from . import settings


def process_order(request):
    """This view should receive 'order_id' via POST, and optionally 'backend' too.
    It will use a signal to ask for filling in the payment details."""
    try:
        order = Order.objects.get(pk=request.POST['order_id'])
    except (Order.DoesNotExist, KeyError):
        return HttpResponseNotFound()
    payment = payment_from_order(order)
    payment.save()
    data = {}
    try:
        data['backend'] = request.POST['backend']
    except KeyError:
        pass
    url = reverse('mamona-process-payment', kwargs={'payment_id': payment.id})
    url = urlunparse((None, None, url, None, urlencode(data), None))
    return HttpResponseRedirect(url)


def prepare(request, ct_pk, obj_pk):
    ct = get_object_or_404(ContentType, pk=ct_pk)
    Payment = ct.model_class()  # Payment is some subclass of PaymentBase
    payment = get_object_or_404(Payment, pk=obj_pk, status=Payment.NEW)


    """This view processes the specified payment. It checks for backend, validates
    it's availability and asks again for it if something is wrong."""
    payment = get_object_or_404(Payment, id=payment_id, status="new")
    if request.method == "POST" or request.REQUEST.has_key("backend"):
        data = request.REQUEST
    elif len(settings.ACTIVE_BACKENDS) == 1:
        data = {"backend": settings.ACTIVE_BACKENDS[0]}
    else:
        data = None
    form = PaymentMethodForm(data=data, payment=payment)
    if form.is_valid():
        form.save()
        ct = ContentType.objects.get_for_model(self.payment)
        return redirect(reverse("mamona:directone:callback",
                                kwargs={"ct_pk": ct.pk, "obj_pk": payment.pk}))
    return direct_to_template(request, "mamona/select_payment_method.html",
                              {"payment": payment, "form": bknd_form})


def confirm(request, ct_pk, obj_pk):
    ct = get_object_or_404(ContentType, pk=ct_pk)
    Payment = ct.model_class()  # Payment is some subclass of PaymentBase
    payment = get_object_or_404(Payment, pk=obj_pk, status=Payment.NEW)
    form = payment.create_form()
    return direct_to_template(request, "mamona/confirm.html",
                              {"form": form, "payment": payment})


def detail(request, ct_pk, obj_pk):
    ct = get_object_or_404(ContentType, pk=ct_pk)
    payment = get_object_or_404(ct.model_class(), pk=obj_pk)
    return HttpResponse("Payment: " + payment.status)
