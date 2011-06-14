from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from payme.backends import Backend


class DirectOneBackend(Backend):
    name = _("DirectOne")

    @property
    def form_class(self):
        from .forms import DirectOneConfirmationForm
        return DirectOneConfirmationForm

    @property
    def reply_url(self):
        return reverse("payme:securepay:success")

    @property
    def _url(self):
        return reverse("payme:securepay:failure")
