import threading
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import StrAndUnicode


# A list of all Backend [sub]classes
ALL = []


class BackendRegistrationMetaclass(type):
    """
    A metaclass that keeps track of all Backend [sub]classes.

    It also adds a *class_path* attribute to the class that its full module path,
    e.g. django_payme.backends.securepay.SecurePayBackend
    """
    def __new__(self, name, bases, attrs):
        cls = type.__new__(self, name, bases, attrs)
        cls.class_path = cls.__module__ + '.' + cls.__name__
        if not attrs.get('abstract', False):
            with threading.RLock():
                ALL.append(cls)
        return cls


class Backend(StrAndUnicode):
    """
    Base class for all backends.

    To exclude a backend from automatically being added to the ``ALL`` list,
    add ``abstract = True`` to the class.
    """
    __metaclass__ = BackendRegistrationMetaclass
    abstract = True
    name = _("Abstract Backend")

    def __unicode__(self):
        return self.name

    def create_form(self, payment):
        return self.form_class(payment=payment, backend=self)

    @property
    def form_class(self):
        from payme.forms import ConfirmationFormBase
        return ConfirmationFormBase
