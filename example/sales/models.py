from django.db import models
from mamona.models import build_payment_model
from ..order.models import UnawareOrder
from . import listeners


# We build the final Payment model here, in external app,
# without touching the code containing UnawareObject.
Payment = build_payment_model(UnawareOrder, related_name='payments')
