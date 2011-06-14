from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from payme.backends import Backend


class SecurePayBackend(Backend):
    name = _("Secure Pay")

    @property
    def form_class(self):
        from .forms import SecurePayConfirmationForm
        return SecurePayConfirmationForm
