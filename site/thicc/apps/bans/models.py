from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from time import timezone

# from .etc import getSteamFrom64

@python_2_unicode_compatible
class Ban(models.Model):

    # for mysql
    # bid        = models.IntegerField(primary_key=True)
    # ip         = models.CharField(max_length=32)
    # authid     = models.CharField(max_length=64)
    # name       = models.CharField(max_length=128)
    # created    = models.IntegerField(max_length=11)
    # ends       = models.IntegerField(max_length=11)
    # length     = models.IntegerField(max_length=10)
    # reason     = models.TextField()
    # aid        = models.IntegerField(max_length=6)
    # adminIp    = models.CharField(max_length=32)
    # sid        = models.IntegerField(max_length=6)
    # country    = models.CharField(max_length=4)
    # RemovedBy  = models.IntegerField(max_length=8)
    # RemoveType = models.CharField(max_length=3)
    # RemovedOn  = models.IntegerField(max_length=10)
    # type       = models.SmallIntegerField(max_length=4)
    # ureason    = models.TextField()

    # for sqlite
    bid = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=32, null=True)
    authid = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    created = models.IntegerField()
    ends = models.IntegerField()
    length = models.IntegerField()
    reason = models.TextField()
    aid = models.IntegerField()
    adminIp = models.CharField(max_length=32)
    sid = models.IntegerField(null=False, default=0)
    country = models.CharField(max_length=4, null=True)
    RemovedBy = models.IntegerField(null=True)
    RemoveType = models.CharField(max_length=3,null=True)
    RemovedOn = models.IntegerField(null=True)
    type = models.SmallIntegerField(null=False, default=0)
    ureason = models.TextField(null=True)
    # comments   = models.TextField(null=True, blank=True)


    class Meta:
        ordering            = ["-created"]
        verbose_name        = "Game-only Ban"
        verbose_name_plural = "Game-only Bans"

    def __str__(self):
        return self.name




@python_2_unicode_compatible
class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    ban = models.ForeignKey(Ban, related_name='comments', verbose_name=_('Ban'))
    ip = models.CharField(max_length=32)
    created = models.IntegerField()
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_commenter', verbose_name=_('Commenter'))
    comment = models.TextField()

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return "{}: {}".format(self.commenter, self.comment)

@python_2_unicode_compatible
class Group(models.Model):
    FLAG_CHOICES = (
        ('a', 'Reserved slot access'),
        ('b', 'Generic admin; required for admins'),
        ('c', 'Kick other players'),
        ('d', 'Ban other players'),
        ('e', 'Remove bans'),
        ('f', 'Slay/harm other players'),
        ('g', 'Change the map or major gameplay features'),
        ('h', 'Change most cvars'),
        ('i', 'Execute config files'),
        ('j', 'Special chat privileges'),
        ('k', 'Start or create votes'),
        ('l', 'Set a password on the server'),
        ('m', 'Use RCON commands'),
        ('n', 'Change sv_cheats or use cheating commands'),
        ('z', 'Magically enables all flags and ignores immunity values'),
    )
    id           = models.AutoField(primary_key=True)
    flags        = models.CharField(max_length=32)
    immunity     = models.IntegerField()
    name         = models.CharField(max_length=120, unique=True)
    textual_name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.textual_name


@python_2_unicode_compatible
class Admin(models.Model):
    aid     = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='ban_admin', verbose_name=_('Thicc Admin'))
    user    = models.CharField(max_length=64, unique=True)
    authid  = models.CharField(max_length=64, unique=True)
    srv_group = models.ForeignKey(Group, related_name='ban_group', verbose_name=_('Group'))
    srv_flags = models.CharField(max_length=64)
    immunity = models.IntegerField(default=50)


    class Meta:
        ordering = ["aid"]
        verbose_name = "In-Game Admin"
        verbose_name_plural = "In-Game Admins"

    def __str__(self):
        return self.aid.username
