'''
Created on 28/03/2011

@author: smf
'''
from django.test import TestCase
from nes_phone.phone_roam.models import Subscription

class ModelTest(TestCase):
    """Tests for the Subscriptions method"""

    fixtures = ['test_subscriptions.json']
    
    def testNoSubscription(self):
        """Verify correct exception is raised when there's no subscriptions in the table for that phone number """
        #self.assertRaises(Exception, Subscription.objects.get(real_number="666777666"))
        pass
        
    def test_subscription(self):
        """Verify there's the subscription in the table"""
        subscription = Subscription.objects.get(real_number="666777888")
        self.assertEqual("666777888", subscription.real_number)
        self.assertEqual("666777999", subscription.log_number)

    
    