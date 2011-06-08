from mamona.utils import get_backend_settings
from . import forms
from . import settings


def get_confirmation_form(payment):
    return {'form': forms.SecurePayConfirmationForm(payment=payment),
            'method': 'post', 'action': settings.URL}
