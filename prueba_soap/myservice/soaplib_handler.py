'''
Created on 02/04/2011

@author: Susana
'''
import StringIO
from django.http import HttpResponse
from soaplib.wsgi import Application
from soaplib.service import rpc, DefinitionBase
from soaplib.serializers import primitive as soap_types
from soaplib.serializers.clazz import Array, ClassSerializer
from soaplib.serializers.primitive import String, Integer


class DumbStringIO(StringIO.StringIO):
    def read(self, n):
        print 'DumbStringIO --> ' + self.getvalue()
        return self.getvalue()

class Permission(ClassSerializer):
    application = String
    feature = String

global_permission = Permission()

class DjangoSoapService(DefinitionBase):

    __tns__ = 'http://127.0.0.1:8000'

    @rpc(Permission, _returns=Permission)
    def get_permision(self, permission):
        print 'get_permission'
        global global_permission
        global_permission.application ='GLOBAL application'
        global_permission.feature = 'GLOBAL feature'
        print global_permission.application
        print global_permission.feature
        print 'parametros'
        print permission.application
        print permission.feature

        return permission

class MySOAPService(Application):
    """
        Creates a WSGI application interface to the SOAP service
    """
    def __call__(self, request):
        print "__call__"
        django_response = HttpResponse()
        def start_response(status, headers):
            status, reason = status.split(' ', 1)
            django_response.status_code = int(status)
            for header, value in headers:
                django_response[header] = value
        environ = request.META.copy()
        body = request.raw_post_data
        environ['CONTENT_LENGTH'] = len(body)
        environ['wsgi.input'] = DumbStringIO(body)
        environ['wsgi.multithread'] = False
        print len(body)
        print DumbStringIO(body)
        response = super(MySOAPService, self).__call__(environ,start_response)
        django_response.content = "\n".join(response)
        print "response --> "+django_response.content
        return django_response