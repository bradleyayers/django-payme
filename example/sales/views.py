from django.conf import settings
from django.http import HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from payme.forms import PaymentBackendForm
from example.order.models import UnawareOrder
from .forms import ItemFormSet
from .models import Payment

import random


def order_singleitem(request):
    # approach 1: single item purchase with predefined backend
    order = UnawareOrder.objects.create()
    order.item_set.create(name="Donation for django-payme author",
                          price=random.random() * 8 + 2)
    payment = Payment(
            order=order,
            backend_class_path="payme.backends.directone.DirectOneBackend")
    payment.full_clean()
    payment.save()
    return direct_to_template(request, "sales/order_singleitem.html",
                              {"order": order, "payment": payment})


def order_multiitem(request):
    # approach 2: an order with no payment method (django-payme will ask)
    order = UnawareOrder()
    if request.method == "POST":
        items_formset = ItemFormSet(instance=order, data=request.POST)
        if items_formset.is_valid():
            order.save()
            items_formset.save()
            payment = Payment(order=order)
            payment.full_clean()
            payment.save()
            return redirect("payme:prepare", ct_pk=payment.content_type.pk,
                            obj_pk=payment.pk)
    else:
        items_formset = ItemFormSet(instance=order)
    return direct_to_template(request, "sales/order_multiitem.html",
                              {"order": order, "items_formset": items_formset})


def order_singlescreen(request):
    # approach 3: single screen (ask for everything)
    if request.method == "POST":
        order = UnawareOrder()
        payment = Payment()
        items_formset = ItemFormSet(data=request.POST, instance=order)
        backend_form = PaymentBackendForm(data=request.POST, instance=payment)
        if items_formset.is_valid() and backend_form.is_valid():
            order.save()
            payment.order = order
            items_formset.save()
            backend_form.save(commit=False)
            payment.full_clean()
            payment.save()
            return redirect("payme:confirm", ct_pk=payment.content_type.pk,
                            obj_pk=payment.pk)
    else:
        backend_form = PaymentBackendForm()
        items_formset = ItemFormSet()
    return direct_to_template(
            request, "sales/order_singlescreen.html",
            {"items_formset": items_formset, "backend_form": backend_form})
