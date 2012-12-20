# Create your views here.    
from django.shortcuts import render_to_response
from nes_phone.common.utils import get_post_values
from nes_phone.nes_api_rest.manager import NESManager
from nes_phone.nes_api_rest.data import NESException, JSONException
from django.http import HttpResponse
from nes_phone.nes_api_rest.json_utilities import CustomEncoder
import logging

log = logging.getLogger("view")

def show_messages(request):
    '''vista de la pagina principal'''
    
    log.debug("show_messages")
    
    
    return render_to_response("messages.html",)


def control_messages(request):
    '''vista para enviar el mensaje a la url de Jajah'''
    
    log.debug("control_messages")
    try:
        request_message = get_post_values(request,'message', "")
        log.debug('message' + request_message)
        manager = NESManager()
        manager.send_text_message(request_message)
        mimetype = 'text/plain'
        return HttpResponse("", mimetype)


    except NESException as inst:
     
        jsonException = CustomEncoder().encode(JSONException(inst))
        log.debug(jsonException)
        return HttpResponse(content=jsonException, mimetype=mimetype, status=inst.code)
    except Exception as e:
     
        log.debug(e.value)
        return HttpResponse(content=e.value, mimetype=mimetype)
    