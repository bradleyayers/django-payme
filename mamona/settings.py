from django.conf import settings


ACTIVE_BACKENDS = getattr(settings, "MAMONA_ACTIVE_BACKENDS", ())
BACKENDS_SETTINGS = getattr(settings, "MAMONA_BACKENDS_SETTINGS", {})
USE_SANDBOX = getattr(settings, "MAMONA_USE_SANDBOX", True)

