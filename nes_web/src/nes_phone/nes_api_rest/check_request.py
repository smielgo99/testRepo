'''
Created on May 19, 2010

@author: mpv
'''

from nes_phone.nes_api_rest.data import NESException, JSONException
from nes_phone.nes_api_rest.json_utilities import CustomEncoder
from django.utils.datastructures import MultiValueDictKeyError


def check_request_type(request, class_name, method_type):
    if request.method != method_type:
        nesException = NESException('METHOD_NOT_SUPPORTED',class_name,'Received ' + request.method + ' method, only ' + method_type +' is supported')
        jsonException = JSONException(nesException)
        json = CustomEncoder().encode(jsonException)
        status_code=405
        return status_code,json
    
    return 200,None