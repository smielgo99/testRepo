# Create your views here.
from django.views.decorators.csrf import csrf_exempt 


from myservice.soaplib_handler import DjangoSoapService, MySOAPService

# the view to use in urls.py
my_soap_service = csrf_exempt(MySOAPService([DjangoSoapService], DjangoSoapService.__tns__)) 

