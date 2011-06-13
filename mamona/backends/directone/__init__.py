from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from mamona.backends import Backend
from .forms import DirectOneConfirmationForm


class DirectOneBackend(Backend):
    FORM_CLASS = DirectOneConfirmationForm

    def __unicode__(self):
        return _("Secure Pay")

    @property
    def reply_url(self):
        return reverse("mamona:securepay:success")

    @property
    def _url(self):
        return reverse("mamona:securepay:failure")
