'''
Created on 14/05/2011

@author: susana
'''
from suds.client import Client

from user import Permission
client = Client('http://localhost:7789/?wsdl')

per = client.factory.create('ns0:Permission')
print per

per.application='mi aplicacion'
per.feature='mi feature'
result = client.service.get_permision(per)
print result
