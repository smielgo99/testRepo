'''
Created on 28/03/2011

@author: smf
'''
from django.contrib import admin
from nes_phone.phone_roam.models import Subscription, ActiveSubscription

'''clases que queremos gestionar desde la herramienta de administracion'''

class SubscriptionsInline(admin.TabularInline):
    model = Subscription
    

admin.site.register(Subscription)
class ActiveSubscriptionsInline(admin.TabularInline):
    model = Subscription
    

admin.site.register(ActiveSubscription)
