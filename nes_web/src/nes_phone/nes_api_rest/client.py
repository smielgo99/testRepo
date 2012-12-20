'''
Created on 29/03/2011

@author: smf
'''
from restful_lib import Connection

class NESClient(object):
    '''
    classdocs
    '''


    def __init__(self, appId, servId):
        '''
        Constructor
        '''
        self.ip="pre.3rd.services.telefonica.es"
        self.port="444"
        self.protocol="https"
        self.path="/services/BA/REST/UCSS/UCSSServer/"
        self.appId = appId
        self.servId = servId 
        self.headers = {'appId' : self.appId, 'servId' : self.servId}
        
    def set_connection(self):
        self.base_url= self.protocol + "://" + self.ip +":"+ str(self.port) + self.path
        self.conn = Connection(self.base_url, username='jajah', password='j4j4h')
        
    def create_subscription(self, json_data):
        
        response = self.conn.request_post("nes/subscriptions/",body=json_data, headers=self.headers)
        print "create_subscription"
        
        return response['headers']['status'], response['headers']['location'], response['body']
    
    def delete_subscription(self, correlators_list):
        
        response = self.conn.request_delete("nes/subscriptions?correlators="+correlators_list, headers=self.headers)
        print "delete_subscription"
        
        return response['headers']['status'], response['body']
    
class JajahTTSClient(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.ip="184.73.181.226"
        self.port="8090"
        self.protocol="http"
        self.path="/text.php"
        
    def set_connection(self):
        self.base_url= self.protocol + "://" + self.ip +":"+ str(self.port) + self.path
        self.conn = Connection(self.base_url)
    
    def send_text_message_to_jajah_tts(self,message):
        response = self.conn.request_get("?text="+message)
        return response['headers']['status'], response['body']
    
class LocalClient(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ip="localhost"
        self.port="81"
        self.protocol="http"
        self.path="/nes_server"
         
        
    def set_connection(self):
        self.base_url= self.protocol + "://" + self.ip +":"+ str(self.port) + self.path
        self.conn = Connection(self.base_url)
        
    def create_subscription(self, json_data):
        response = self.conn.request_post("/subs.json")
        response['headers']['location']="http://212.179.159.77/nesphase2/nes/subscriptions/1234567891321"
        return response['headers']['status'],response['headers']['location'], response['body']

    def delete_subscription(self, correlators_list):
        
        return 200, "{}"    