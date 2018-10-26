from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

@python_2_unicode_compatible
class ScapePlayer(models.Model):
    id       = models.IntegerField(primary_key=True)
    name     = models.CharField(max_length=13)
    duration = models.BigIntegerField()
    donator  = models.IntegerField()
    staff    = models.IntegerField()

    class Meta:
        ordering = ["duration"]

    def __str__(self):
        return self.name