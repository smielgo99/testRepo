# Create your views here.    

from django.http import HttpResponse
from nes_phone.nes_api_rest.check_request import check_request_type
from nes_phone.nes_api_rest.json_utilities import CustomEncoder
from nes_phone.nes_api_rest.manager import NESManager

import logging


log = logging.getLogger("nes_api_rest.views")
def handle(request):
    ''' expone la interfaz como parte servidora para gestionar las peticiones handelCallEvent'''
    
    log.debug("handle")    
    
    #Check that is a POST request
    status_code, json_data =check_request_type(request,'views.tags','POST')
    
    if(status_code == 200):
        nes_manager = NESManager()
        status_code, result = nes_manager.handle(request)
        
        #transform to json string
        json_data = CustomEncoder().encode(result)
        log.debug('json_data: '+ json_data)

    #json_data = '{"action": {"announcementId": "3", "callingPartyAddress":{"phoneNumber": "0034600222200"}, "defaultErrorHandling": true, "legId":"1", "actionToPerform": "OnHold"}, "callSessionIdentifier":"129916513689383"}'   
    response = HttpResponse(json_data,mimetype="application/json",status = status_code)     
    return response

