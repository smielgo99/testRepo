'''
Created on 30/03/2011

@author: Susana
'''
import json
from nes_phone.phone_roam.models import Subscription
from django.core.exceptions import ObjectDoesNotExist
from nes_phone.nes_api_rest.data import ActionType, UserIdType, HandleCallEventResponse
from nes_phone.nes_api_rest.json_utilities import CustomEncoder

from nes_phone.nes_api_rest.data import NESException, JSONException
from django.conf import settings
import logging
import urllib


log = logging.getLogger("NESManager")

class NESManager(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass
        
    
    def handle(self, request):
        '''
        procesa los handlesCallEvent para el phoneRoaming. Actua como servidor
        
            real_number = A
            log_number = B
            if real_number = calledParticipant
                incoming call to real_number
            if real_number = calledParticipant
                incoming call to log_number
            if real_mubner = callingParticipant
                outgoing from real_number
        '''
        log.debug("Inicio handle")
                
        json_data = json.loads(request.raw_post_data)
        log.debug("json_data: " + str(json_data) )
        called =  json_data['callEvent']['calledParticipant']['phoneNumber']
        calling = json_data['callEvent']['callingParticipant']['phoneNumber']
        callSessionID = json_data['callEvent']['callSessionID']
        
        PREFIX = getattr(settings, 'PREFIX')
        #quitamos el prefijo
        calledParticipant= called[called.find(PREFIX)+len(PREFIX):]
        callingParticipant = calling[calling.find(PREFIX)+len(PREFIX):]
        
        
        log.debug('called: ' + called)
        log.debug('calling: ' +  calling)
        log.debug('calledParticipant: ' +  calledParticipant)
        log.debug('callingParticipant: ' +  callingParticipant)
        log.debug('callSessionID: ' +  callSessionID)
        
        
        routingAddress =""
        callingPartyAddress = ""
        
        #Consultar la bd para ver las subscripciones
        try:
            subscription = Subscription.objects.get(real_number=calledParticipant)
            routingAddress = UserIdType()
            routingAddress.phoneNumber = calledParticipant
            callingPartyAddress = UserIdType()
            callingPartyAddress.phoneNumber = u'#'+callingParticipant
        except ObjectDoesNotExist: 
            try:
                subscription = Subscription.objects.get(log_number=calledParticipant)
                routingAddress = UserIdType()
                routingAddress.phoneNumber = subscription.real_number
                callingPartyAddress = UserIdType()
                callingPartyAddress.phoneNumber = callingParticipant
            except ObjectDoesNotExist: 
                try:
                    subscription = Subscription.objects.get(real_number=callingParticipant)
                    routingAddress = UserIdType(calledParticipant)
                    callingPartyAddress = UserIdType(subscription.log_number)
                except ObjectDoesNotExist: 
                    #TODO: tiene que dar una excepcion porque no funciona el handle RAISE NESException
                    print ObjectDoesNotExist
                    nesException = NESException('400', 'Error', 'El numero no existe en la BD')
                    jsonException = JSONException(nesException)
                    return 400,jsonException
                
        '''
        {"action": 
            {"announcementId": "3", 
             "callingPartyAddress": 
                    {"phoneNumber": "0034600222200"}, 
             "errorHandling": true, 
             "legId":"1", 
             "actionToPerform": "OnHold"
            }, 
         "callSessionID":"129916513689383"}
        '''
        log.debug("routingAddress.phoneNumber "+ routingAddress.phoneNumber)
        log.debug("callingPartyAddress.phoneNumber "+ callingPartyAddress.phoneNumber)
        
        transactionId = "0123456789" #TODO cambiar por algo que no sea fijo
        action_type = ActionType("Route", transactionId)
        action_type.legId="2"
        action_type.routingAddress = routingAddress
        action_type.callingPartyAddress = callingPartyAddress
        action = HandleCallEventResponse(action_type)
        action.callSessionID = callSessionID
        return 200, action


    def get_json_parameters(self, json_data, param, default_value):
        try:
            param_value = json_data[param]
        except: 
            param_value = default_value
        return param_value
    
    def save_subscription(self, subscription):
        '''
        procesa las peticiones y la comunicacion con el FW3rd y el NES para guardar las suscripciones en la BD del NES
        Actua como cliente
        '''
        
        log.debug('save_subscription')
        try:
            json_data = CustomEncoder().encode(subscription)
        
            log.debug('json_data: '+json_data)
            IS_REAL_SERVER = getattr(settings, 'IS_REAL_SERVER')
            if IS_REAL_SERVER:
                from nes_phone.nes_api_rest.client import NESClient
                connect = NESClient("123","456")     
            else:
                from nes_phone.nes_api_rest.client import LocalClient
                connect = LocalClient()
            connect.set_connection()  
            
            status, location, service_json = connect.create_subscription(json_data)
            if status !='200':
                raise NESException(status, 'save_subscription', 'Error save_subscription')
            #service_json = json.loads(service_json)
            #correlator = service_json['correlator']
            #print correlator
            correlator = location[location.find("nes/subscriptions/")+len("nes/subscriptions/"):]
            return correlator
        except NESException as inst:
            
            raise inst
        
    def delete_subscription(self, correlators_list):
        '''
        procesa las peticiones y la comunicacion con el FW3rd y el NES para borrar las suscripciones del BD del NES
        Actua como cliente
        '''
        log.debug('delete_subscription')
        IS_REAL_SERVER = getattr(settings, 'IS_REAL_SERVER')
        
        if IS_REAL_SERVER:
            from nes_phone.nes_api_rest.client import NESClient
            connect = NESClient("123","456")     
        else:
            from nes_phone.nes_api_rest.client import LocalClient
            connect = LocalClient()
            
        connect.set_connection()
        connect.delete_subscription(correlators_list)
    
    def send_text_message(self, message):
        ''' manda un texto al endpoint de Jajah para transformar el texto a voz'''
        
        log.debug('send_text_message')
        
        #URL escaped 
        text = urllib.quote(message)

        IS_REAL_SERVER = getattr(settings, 'IS_REAL_SERVER')
        
        if IS_REAL_SERVER:
            from nes_phone.nes_api_rest.client import JajahTTSClient
            connect = JajahTTSClient()     
        else:
            from nes_phone.nes_api_rest.client import LocalClient
            connect = LocalClient()
            
        connect.set_connection()
        status, body = connect.send_text_message_to_jajah_tts(text)
        
        if status !='200':
                raise NESException(status, 'save_subscription', 'Error save_subscription')
