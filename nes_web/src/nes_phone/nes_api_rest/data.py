'''
Created on 30/03/2011

@author: smf
'''
import logging


class JSONException(object):
    def __init__(self, exception):
        self.exception=exception

class NESException(Exception):
    '''
    classdocs
    '''
    def __init__(self, code, class_name, message):
        '''
        Constructor
        '''
        self.code = code
        self.class_name = class_name
        self.message = message
        logging.warn('EXCEPTION ' + self.code + ' ' + self.class_name + ' ' + self.message)

class StartCallNotification(object):
    

    def __init__(self, startCallNotificationRequest):
        '''
        Constructor
        '''
        self.startCallNotification = startCallNotificationRequest
        
class StartCallNotificationRequest(object):
    
    '''
       <xsd:complexType name="ParlayX.startCallNotificationRequest">
        <xsd:sequence>
         <xsd:element maxOccurs="1" minOccurs="1" name="reference" type="tns:ParlayX.ReferenceType"/>
         <xsd:element maxOccurs="1" minOccurs="1" name="monitoredParty" type="tns:ParlayX.UserIdType"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="directionMode" nillable="true" type="xsd:boolean"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="addressDirection" nillable="true" type="tns:ParlayX.AddressDirectionType"/>
         <xsd:element maxOccurs="unbounded" minOccurs="0" name="criteria" nillable="true" type="tns:ParlayX.CallEventsType"/>
         <xsd:element maxOccurs="unbounded" minOccurs="0" name="otherParties" nillable="true" type="tns:ParlayX.UserIdType"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="regexpEnabled" nillable="true" type="xsd:boolean"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="roamingCondition" nillable="true" type="tns:ParlayX.RoamingConditionType"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="defaultOnHold" nillable="true" type="xsd:boolean"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="announcementId" nillable="true" type="tns:ParlayX.AnnouncementIdType"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="defaultCallHandling" nillable="true" type="xsd:boolean"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="digitsConfiguration" nillable="true" type="tns:ParlayX.DigitsConfigurationType"/>
        </xsd:sequence>
       </xsd:complexType>
    '''

    def __init__(self, reference, monitoredParty):
        '''
        Constructor
        '''
        self.reference = reference
        self.monitoredParty = monitoredParty

        
     
class ReferenceType(object):
    '''
       <xsd:complexType name="ParlayX.ReferenceType">
        <xsd:sequence>
         <xsd:element maxOccurs="1" minOccurs="1" name="endpoint" nillable="true" type="xsd:string"/>
         <xsd:element maxOccurs="1" minOccurs="1" name="interfaceName" nillable="true" type="xsd:string"/>
        </xsd:sequence>
       </xsd:complexType>
    '''
    def __init__(self, endpoint):
        self.endpoint = endpoint

        
    

class UserIdType(object):
    
    '''
       <xsd:complexType name="ParlayX.UserIdType">
        <xsd:sequence>
         <xsd:element maxOccurs="1" minOccurs="1" name="phoneNumber" nillable="true" type="xsd:string"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="anyUri" nillable="true" type="xsd:anyURI"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="ipAddress" nillable="true" type="tns:ParlayX.IpAddressType"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="alias" nillable="true" type="xsd:string"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="otherId" nillable="true" type="tns:ParlayX.OtherIdType"/>
        </xsd:sequence>
       </xsd:complexType>
   '''
   
    def __init__(self): 
        pass

class AddressDirectionType(object):   
    '''
       <xsd:simpleType name="ParlayX.AddressDirectionType">
        <xsd:restriction base="xsd:string">
         <xsd:enumeration value="Called"/>
         <xsd:enumeration value="Calling"/>
         <xsd:enumeration value="Both"/>
        </xsd:restriction>
       </xsd:simpleType>
   '''
    
    Called="Called"
    Calling="Called"
    Both="Called"
class CallEventsType(object):
    '''
       <xsd:simpleType name="ParlayX.CallEventsType">
        <xsd:restriction base="xsd:string">
         <xsd:enumeration value="Busy"/>
         <xsd:enumeration value="NotReachable"/>
         <xsd:enumeration value="NoAnswer"/>
         <xsd:enumeration value="CalledNumber"/>
         <xsd:enumeration value="Answer"/>
         <xsd:enumeration value="Disconnected"/>
         <xsd:enumeration value="Ringing"/>
         <xsd:enumeration value="Abandon"/>
         <xsd:enumeration value="CollectedData"/>
         <xsd:enumeration value="RouteSelectFailure"/>
         <xsd:enumeration value="EndOfAnnouncement"/>
        </xsd:restriction>
       </xsd:simpleType>
    '''
    Busy="Busy"
    NotReachable="NotReachable"
    NoAnswer="NoAnswer"
    CalledNumber="CalledNumber"
    Answer="Answer"
    Disconnected="Disconnected"
    Ringing="Ringing"
    Abandon="Abandon"
    CollectedData="CollectedData"
    RouteSelectFailure="RouteSelectFailure"
    EndOfAnnouncement="EndOfAnnouncement"
    Exception="Exception"
    
    
class RoamingConditionType(object):
    '''
       <xsd:simpleType name="ParlayX.RoamingConditionType">
        <xsd:restriction base="xsd:string">
         <xsd:enumeration value="OnlyRoaming"/>
         <xsd:enumeration value="OnlyNotRoaming"/>
         <xsd:enumeration value="RoamingIndependent"/>
        </xsd:restriction>
       </xsd:simpleType>
    '''
    OnlyRoaming="OnlyRoaming"
    OnlyNotRoaming="OnlyRoaming"
    RoamingIndependent="OnlyRoaming"
      
      
class AnnouncementIdType(object):    
    '''  
       <xsd:complexType name="ParlayX.AnnouncementIdType">
        <xsd:sequence>
         <xsd:element maxOccurs="1" minOccurs="0" name="integer" nillable="true" type="xsd:int"/>
        </xsd:sequence>
       </xsd:complexType>
    '''      
    def __init__(self, id):
        self.AnnouncementId=id
         
         
class ActionType(object):
    '''
       <xsd:complexType name="ParlayX.ActionType">
        <xsd:sequence>
         <xsd:element maxOccurs="1" minOccurs="1" name="actionToPerform" type="tns:ParlayX.ActionValuesType"/>
         <xsd:element maxOccurs="1" minOccurs="1" name="transactionId" nillable="true" type="xsd:string"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="routingAddress" nillable="true" type="tns:ParlayX.UserIdType"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="callingPartyAddress" nillable="true" type="tns:ParlayX.UserIdType"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="legId" nillable="true" type="xsd:int"/>
         <xsd:element maxOccurs="unbounded" minOccurs="0" name="legIdSet" nillable="true" type="xsd:int"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="chargingCode" nillable="true" type="tns:ParlayX.ChargingCodeType"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="announcementId" nillable="true" type="tns:ParlayX.AnnouncementIdType"/>
         <xsd:element maxOccurs="unbounded" minOccurs="0" name="announcementLegs" nillable="true" type="xsd:int"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="errorHandling" nillable="true" type="xsd:boolean"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="recordingConfiguration" nillable="true" type="tns:ParlayX.RecordingConfigurationType"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="mediaRecordingIdentifier" nillable="true" type="xsd:string"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="digitsConfiguration" nillable="true" type="tns:ParlayX.DigitsConfigurationType"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="ignoreNextCallEvents" nillable="true" type="xsd:boolean"/>
        </xsd:sequence>
       </xsd:complexType>
    '''
    def __init__(self, actionToPerform, transactionId):
        self.actionToPerform = actionToPerform
        self.transactionId = transactionId

        
        
class ActionValuesType(object):        

    Continue = "Continue"
    Route = "Route"
    OnHold = "OnHold"
    EndCall = "EndCall"
    RouteLeg = "RouteLeg"
    ConnectLegs = "ConnectLegs"
    RemoveLeg = "RemoveLeg"
    ConnectAndRemove = "ConnectAndRemove"
    PlayAndRecord = "PlayAndRecord"
    StopPlayAndRecord = "StopPlayAndRecord"
    PlayAndCollect = "PlayAndCollect"
    
class DigitsConfigurationType(object):
    
    '''
       <xsd:complexType name="ParlayX.DigitsConfigurationType">
        <xsd:sequence>
         <xsd:element maxOccurs="1" minOccurs="0" name="maxDigits" nillable="true" type="xsd:int"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="minDigits" nillable="true" type="xsd:int"/>
         <xsd:element maxOccurs="1" minOccurs="1" name="interruptMedia" type="xsd:boolean"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="startDigit" nillable="true" type="xsd:string"/>
         <xsd:element maxOccurs="1" minOccurs="0" name="stopDigit" nillable="true" type="xsd:string"/>
        </xsd:sequence>
       </xsd:complexType>
   
   '''
   
    def __init__(self, interruptMedia): 
        
        self.interruptMedia = interruptMedia
        
        
class HandleCallEventResponse(object):
    '''
       <xsd:complexType name="UCSS.handleCallEventResponse">
        <xsd:sequence>
         <xsd:element maxOccurs="1" minOccurs="1" name="result" type="tns:UCSS.ActionType"/>
        </xsd:sequence>
       </xsd:complexType>
    '''
    
    def __init__(self, actionType):
        self.action = actionType
        