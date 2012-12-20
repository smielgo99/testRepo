'''
Created on 29/03/2011

@author: smf
'''
from django.test import TestCase
from nes_phone.phone_roam.models import Subscription
from django.db import *
from nes_phone.common.utils import convert_str_to_int, get_parameter_from_request
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client

class RequestFactory(Client):
    """
    Class that lets you create mock Request objects for use in testing.
    
    Usage:
    
    rf = RequestFactory()
    get_request = rf.get('/hello/')
    post_request = rf.post('/submit/', {'foo': 'bar'})
    
    This class re-uses the django.test.client.Client interface, docs here:
    http://www.djangoproject.com/documentation/testing/#the-test-client
    
    Once you have a request object you can pass it to any view function, 
    just as if that view had been hooked up using a URLconf.
    
    """

    def request(self, **request):
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'REMOTE_ADDR' : '127.0.0.0',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
        }
        environ.update(self.defaults)
        environ.update(request)
        return WSGIRequest(environ)



class UtilsTest(TestCase):
    def test_get_parameter_from_request(self):
        
        #rf = RequestFactory()
        pass

        