import threading
from django.utils.encoding import StrAndUnicode
from mamona.forms import ConfirmationFormBase


# A list of all Backend [sub]classes
ALL = []


class BackendRegistrationMetaclass(type):
    """
    A metaclass that keeps track of all Backend [sub]classes.

    It also adds a *class_path* attribute to the class that its full module path,
    e.g. mamona.backends.securepay.SecurePayBackend
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
    FORM_CLASS = ConfirmationFormBase

    def create_form(self, payment):
        return self.FORM_CLASS(payment=payment, backend=self)
