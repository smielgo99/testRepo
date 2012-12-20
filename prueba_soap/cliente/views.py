# Create your views here.
from django.http import HttpResponse
from suds.client import Client
from soaplib.serializers.clazz import Array, ClassSerializer
from soaplib.serializers.primitive import String, Integer

class Permission(ClassSerializer):
    application = String
    feature = String
    
def prueba(request):
    client = Client('http://localhost:8080/?wsdl')
    per = client.factory.create('s1:Permission')
    print per
    
    per.application='mi aplicacion'
    per.feature='mi feature'
    result = client.service.get_permision(per)
    print result
    print result.application
      
    response = HttpResponse(result,mimetype="text/plain",status = '200')   
    return response 
    