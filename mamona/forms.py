from django import forms
from django.utils.translation import ugettext as _


class PaymentMethodForm(forms.ModelForm):
    """
    Shows choice field with all active payment backends. You may use it with
    existing Payment instance to push it through all the remaining logic,
    getting the link to the next payment step from proceed_to_gateway() method.
    """
    class Meta:
        fields = ("backend_class", )


class ConfirmationFormBase(forms.Form):
    """
    The final form rendered to a user that will submit to a payment gateway.

    :param payment: a Payment object
    :param backend: a Backend object
    :param method: the form method (default: ``"post"``)
    :param action: the form action (default: ``"http://xyz.com/gateway.asp"``)
    """
    def __init__(self, *args, **kwargs):
        if "payment" not in kwargs or "backend" not in kwargs:
            raise ValueError("%s must be passed 'payment' and 'backend' "
                             "arguments." % self.__class__.__name__)
        self.payment = kwargs.pop("payment")
        self.backend = kwargs.pop("backend")
        # *method* and *action* are used in the <form> tag
        self.method = kwargs.pop("method", "post")
        self.action = kwargs.pop("action", "")
        super(ConfirmationFormBase, self).__init__(*args, **kwargs)
        # The payment is now considered to be "in progress".
        self.payment.status = self.payment.IN_PROGRESS
        self.payment.save()

    def clean(self):
        raise NotImplementedError("This form is not intended to be validated here.")

    def add_hidden_field(self, name, value=None, index=None, **kwargs):
        """
        Utility method to add a hidden input to the form.
        """
        field = forms.CharField(initial=value, widget=forms.HiddenInput(), **kwargs)
        if index is not None:
            self.fields.insert(index, name, field)
        else:
            # adds the field to the tail
            self.fields[name] = field
