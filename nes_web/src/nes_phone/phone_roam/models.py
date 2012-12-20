from django.db import models

# Create your models here.
class Subscription(models.Model):
    real_number = models.CharField(max_length=200)
    log_number = models.CharField(max_length=200)
    def __unicode__(self):
        return u'%s: %s' % (self.real_number, self.log_number)
    
class ActiveSubscription(models.Model):
    phone_number = models.CharField(max_length=20)
    urlcallback = models.CharField(max_length=80)
    subscriptionId = models.CharField(max_length=20)
    direction = models.CharField(max_length=10)
    
    def __unicode__(self):
        return u'%s'  % (self.phone_number)