# Create your views here.
from django.views.decorators.csrf import csrf_exempt 
from soap_service import DjangoSoapService, DumbStringIO
from django.http import HttpResponse
from soaplib.wsgi import Application


class MySOAPService(Application):
    """
Creates a WSGI application interface to the SOAP service
"""
    def __call__(self, request):

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
#        print len(body)
#        print DumbStringIO(body)
        response = super(MySOAPService, self).__call__(environ,start_response)
        django_response.content = "\n".join(response)
#        print "response --> "+django_response.content
        return django_response

my_soap_service = csrf_exempt(MySOAPService([DjangoSoapService], DjangoSoapService.__tns__)) 