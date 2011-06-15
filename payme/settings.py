from django.conf import settings


BACKENDS = getattr(settings, "PAYME_BACKENDS", {})
USE_SANDBOX = getattr(settings, "PAYME_USE_SANDBOX", True)
