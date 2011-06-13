from django.db import models
from mamona.abstract_mixin import AbstractMixin


class DummyTxn(models.Model):
    comment = models.CharField(max_length=100, default="a dummy transaction")

    class Meta:
        app_label = "mamona"
