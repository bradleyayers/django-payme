from django.dispatch import Signal


payment_status_changed = Signal()
payment_status_changed.__doc__ = "Sent when Payment status changes."
