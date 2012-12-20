'''
Created on 02/04/2011

@author: Susana
'''
import StringIO

from soaplib.service import rpc, DefinitionBase
from soaplib.serializers import primitive as soap_types

class DumbStringIO(StringIO.StringIO):
    def read(self, n):
        print 'DumbStringIO --> ' + self.getvalue()
        return self.getvalue()

class DjangoSoapService(DefinitionBase):

    __tns__ = 'http://127.0.0.1:8000'

    @rpc(soap_types.String, _returns=soap_types.String)
    def hello_world(self, hello_string):
        """
        Accepts primitive string and returns the same primitive.
        """
        return hello_string 
    
