'''
Created on 29/03/2011

@author: smf
'''
from django.test import TestCase
from nes_phone.phone_roam.models import Subscription
from nes_phone.phone_roam.views import manage_subscription
from django.db import IntegrityError

class SubscriptionsTest(TestCase):
    """Tests for the Subscriptions method"""
    def test_add_subscription(self):
        """Verify that the subcription is added"""
        
        manage_subscription("666000111", "666000222")
        subscription = Subscription.objects.get(real_number="666000111")
        self.assertEqual("666000111", subscription.real_number)
        self.assertEqual("666000222", subscription.log_number)

    def test_delete_subscription(self):
        """Verify that the subcription is deleted"""
        
        manage_subscription("666000111", None)
        self.assertRaises(IntegrityError, Subscription.objects.get(real_number="666777666"))
        #pass
