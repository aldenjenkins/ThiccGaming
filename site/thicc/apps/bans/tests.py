from django.test import TestCase
from .models import *
from time import time


class BanModelTests(TestCase):


    def test_is_expired_with_currently_expired(self):
        testBan = Ban(ends=1233,
                      length=12312332212,
                      RemovedBy=32,
                      RemovedOn=93,
                      RemoveType='U')
        is_expired = testBan.ends < int(time())
        self.assertIs(is_expired, True)

    def test_is_expired_with_currently_not_expired(self):
        testBan = Ban(name="Flavio Johnson",
                      adminIp="123.123.123.123.123.123.123.123.123.123.123.123.123",
                      aid=432,
                      country="US, A",
                      created=123123,
                      authid=123123123,
                      bid=32,
                      ends=int(time())+1000,
                      length=12312332212,
                      ip="123.123.123.123.123.123.123.123.123.123.123.123.123",
                      reason="i liek..... DA'eggs.",
                      RemovedBy=32,
                      RemovedOn=93,
                      RemoveType='U',
                      sid=2,
                      ureason='Flavio johnson LALALALALAAAAAAAA',
                      type=0)
        is_expired = testBan.ends < int(time())
        self.assertIs(is_expired, False)

    def test_is_unbanned_with_currently_unbanned_while_ban_was_active(self):
        testBan = Ban(name="Flavio Johnson",
                      adminIp="123.123.123.123.123.123.123.123.123.123.123.123.123",
                      aid=432,
                      country="US, A",
                      created=123123,
                      authid=123123123,
                      bid=32,
                      ends=1233,
                      length=12312332212,
                      ip="123.123.123.123.123.123.123.123.123.123.123.123.123",
                      reason="i liek..... DA'eggs.",
                      RemovedBy=32,
                      RemovedOn=93,
                      RemoveType='U',
                      sid=2,
                      ureason='Flavio johnson LALALALALAAAAAAAA',
                      type=0)
        is_unbanned = testBan.RemovedOn < int(time()) and testBan.RemovedOn < testBan.ends
        self.assertIs(is_unbanned, True)

    def test_is_unbanned_with_currently_not_unbanned(self):
        testBan = Ban(name="Flavio Johnson",
                      adminIp="123.123.123.123.123.123.123.123.123.123.123.123.123",
                      aid=432,
                      country="US, A",
                      created=123123,
                      authid=123123123,
                      bid=32,
                      ends=1233,
                      length=12312332212,
                      ip="123.123.123.123.123.123.123.123.123.123.123.123.123",
                      reason="i liek..... DA'eggs.",
                      sid=2,
                      ureason='Flavio johnson LALALALALAAAAAAAA',
                      type=0)
        # This makes sure that if the ban was removed, it was removed while the ban was active.
        is_unbanned = testBan.RemovedOn is not None and testBan.RemovedOn < int(time()) and testBan.RemovedOn < testBan.ends
        self.assertIs(is_unbanned, False)

    def test_is_unbanned_with_currently_unbanned_after_ban_expiration(self):
        testBan = Ban(name="Flavio Johnson",
                      adminIp="123.123.123.123.123.123.123.123.123.123.123.123.123",
                      aid=432,
                      country="US, A",
                      created=123123,
                      authid=123123123,
                      bid=32,
                      ends=1233,
                      length=12312332212,
                      ip="123.123.123.123.123.123.123.123.123.123.123.123.123",
                      reason="i liek..... DA'eggs.",
                      RemovedBy=32,
                      RemovedOn=1234,
                      RemoveType='U',
                      sid=2,
                      ureason='Flavio johnson LALALALALAAAAAAAA',
                      type=0)
        # This makes sure that if the ban was removed, it was removed while the ban was active.
        is_unbanned = testBan.RemovedOn is not None and testBan.RemovedOn < int(time()) and testBan.RemovedOn < testBan.ends
        self.assertIs(is_unbanned, False)
