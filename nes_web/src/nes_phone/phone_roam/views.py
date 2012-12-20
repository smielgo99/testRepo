# Create your views here.    
from django.shortcuts import render_to_response
from nes_phone.phone_roam.models import Subscription, ActiveSubscription
from nes_phone.common.utils import get_post_values
from django.http import HttpResponse
from nes_phone.nes_api_rest.data import ReferenceType, UserIdType, StartCallNotification, StartCallNotificationRequest, CallEventsType
from nes_phone.nes_api_rest.manager import NESManager 
from django.conf import settings
from nes_phone.nes_api_rest.data import NESException, JSONException
from nes_phone.nes_api_rest.json_utilities import CustomEncoder
import logging

log = logging.getLogger("view")

def home(request):
    '''vista de la pagina principal'''
    
    log.debug("home")
    
    try:
        REAL_NUMBER = getattr(settings, 'REAL_NUMBER')
        log.debug("real number: " + REAL_NUMBER)
        subscription = Subscription.objects.get(real_number = REAL_NUMBER)
        subs = subscription.log_number
    except:
        subs = ""
    return render_to_response("home.html",
                              {'active_subscriptions': subs,
                               })
 
def xhr_subscription(request):
    '''peticion procesada por ajax para el control de la creacion y borrado de las suscripciones'''
    
    try:
        log.debug("xhr_subscription")
        
        request_real_number = get_post_values(request,'real_number', "")
        request_log_number = get_post_values(request,'log_number', "")
        request_action = get_post_values(request,'action', "")
        
        PREFIX = getattr(settings, 'PREFIX')
        log.debug( 'prefix '+PREFIX)
        mimetype = 'text/plain'
    
        if request_action == 'POST':
            log.debug('POST')
            create_subscription(PREFIX+request_real_number, PREFIX+request_log_number)
        elif request_action == 'DELETE':
            log.debug('DELETE')
            delete_subscription(PREFIX+request_real_number, PREFIX+request_log_number)
        
        
        subs = manage_subscription(request_real_number, request_log_number)
        
        return HttpResponse(subs, mimetype)


    except NESException as inst:
     
        jsonException = CustomEncoder().encode(JSONException(inst))
        log.debug(jsonException)
        return HttpResponse(content=jsonException, mimetype=mimetype, status=inst.code)
    except Exception as e:
     
        log.debug(e.value)
        return HttpResponse(content=e.value, mimetype=mimetype)
 

def manage_subscription(real_number, log_number):
    ''' controla la tabla suscripciones para crear o borrar la suscripcion'''
    
    log.debug("manage_subscription")
    log.debug("real_number "+real_number)
    try:
        subscription = Subscription.objects.get(real_number=real_number)
        
        subscription.delete();
        log.debug("delete")
        subs = ""
    except:
        if log_number!="":
            
            subscription = Subscription(real_number=real_number, log_number=log_number)
            subscription.save();
            log.debug("save")
        subs = log_number
    return subs    

def create_subscription(real_number, log_number):
    '''
    crea las suscripciones necesarias para el phone roaming:
    - Both: para el numero real
    - Terminante: para el numero logueado
    - Crea las entradas en la tabla ActiveSubscriptions
    '''
    log.debug('create_subscription')
    try:
        #suscripcion en originante y terminante para el numero real
    
        endpoint = "http://212.179.159.77/nesphase2" 
        reference = ReferenceType(endpoint)
        
    
        interface = "ParlayX"
        
        reference.endpoint = endpoint
        reference.interfaceName = interface
        
    
        criteriaList = []
        criteria = CallEventsType()
        criteriaList.append(criteria.CalledNumber);
        
        monitoredParty = UserIdType()
        #phoneNumber
        monitoredParty.phoneNumber = real_number
        startCallNotificationRequest = StartCallNotificationRequest(reference, monitoredParty)
        startCallNotificationRequest.criteria = criteriaList
        startCallNotificationRequest.addressDirection = "Both"
        startCallNotificationRequest.directionMode = True
        subscription = StartCallNotification(startCallNotificationRequest)
        manager = NESManager()
            
        correlator = manager.save_subscription(subscription)   
      
        # guardar el correlator en la BD
            
        active_subscription = ActiveSubscription(phone_number   = subscription.startCallNotification.monitoredParty.phoneNumber, 
                                                 urlcallback    = subscription.startCallNotification.reference.endpoint,
                                                 subscriptionId = correlator,
                                                 direction      = subscription.startCallNotification.addressDirection)
        active_subscription.save();
        
      
        criteriaList = []
        criteria = CallEventsType()
        criteriaList.append(criteria.CalledNumber);
        
        monitoredParty = UserIdType()
        #phoneNumber
        monitoredParty.phoneNumber = log_number
        startCallNotificationRequest = StartCallNotificationRequest(reference, monitoredParty)
        startCallNotificationRequest.criteria = criteriaList
        startCallNotificationRequest.addressDirection = "Called"
        startCallNotificationRequest.directionMode = True
        subscription = StartCallNotification(startCallNotificationRequest)
        correlator = manager.save_subscription(subscription)
        # guardar el correlator en la BD
        
        active_subscription = ActiveSubscription(phone_number   = subscription.startCallNotification.monitoredParty.phoneNumber, 
                                                 urlcallback    = subscription.startCallNotification.reference.endpoint,
                                                 subscriptionId = correlator,
                                                 direction      = subscription.startCallNotification.addressDirection)
        active_subscription.save();
    except NESException as inst:
        print inst.message
        raise inst
    except Exception as inst:
        print inst.message
        raise inst
def delete_subscription(real_number, log_number):   
    '''
    controla el borrado de las suscripciones 
    - recupera los correladores
    - borra las entradas de la tabla ActiveSuscriptions
    - borra la suscripcion del NES
    '''
    log.debug('delete_susbcription')
    #recuperamos los correladores de la BD para el real_number y el log_number
    active_subscription = ActiveSubscription.objects.get(phone_number=real_number)
    active_subscription.delete()
    log.debug( active_subscription )
    
    correlators_list = active_subscription.subscriptionId
    
    active_subscription = ActiveSubscription.objects.get(phone_number=log_number)
    active_subscription.delete()
    log.debug( active_subscription )
    
    correlators_list += ','+active_subscription.subscriptionId
    log.debug( 'correlator_list: '+correlators_list)
    manager = NESManager()
    manager.delete_subscription(correlators_list)
    
    
