from django.conf import settings


BACKENDS = getattr(settings, "MAMONA_BACKENDS", ())
USE_SANDBOX = getattr(settings, "MAMONA_USE_SANDBOX", True)
