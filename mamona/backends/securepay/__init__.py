from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from mamona.backends import Backend
from .forms import SecurePayConfirmationForm


class SecurePayBackend(Backend):
    FORM_CLASS = SecurePayConfirmationForm

    def __unicode__(self):
        return _("Secure Pay")
