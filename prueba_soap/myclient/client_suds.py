'''
Created on 14/05/2011

@author: susana
'''
from suds.client import Client

from soaplib.serializers.clazz import Array, ClassSerializer
from soaplib.serializers.primitive import String, Integer

class Permission(ClassSerializer):
    application = String
    feature = String

client = Client('http://localhost:7789/?wsdl')

per = client.factory.create('ns0:Permission')
print per

per.application='mi aplicacion'
per.feature='mi feature'
result = client.service.get_permision(per)
print result