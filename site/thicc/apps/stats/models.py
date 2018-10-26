from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

@python_2_unicode_compatible
class L4d2Stat(models.Model):
    cid = models.AutoField(primary_key=True)

    class Meta:
        ordering            = ["-created"]
        verbose_name        = "Left 4 Dead 2 Stat"
        verbose_name_plural = "Left 4 Dead 2 Stats"

    def __str__(self):
        return self.cid


"""
We must require that users be registered on FooBarGaming.com with their
steam account to have their stats tracked.
"""
@python_2_unicode_compatible
class GModStat(models.Model):
    player = models.ForeignKey()
    kills = models.IntegerField()

    class Meta:
        ordering            = ["-created"]
        verbose_name        = "Garry's Mod Stat"
        verbose_name_plural = "Garry's Mod Stats"

    def __str__self(self):
        return self.player
