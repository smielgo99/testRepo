'''
Created on 29/03/2011

@author: smf
'''

import time
import random

def convert_str_to_int(s):
    try:
        ret = int(s)
    except ValueError:
        #Try float.
        try:
            ret = float(s)
        except ValueError:
            return s
    return ret
def get_get_values(request, param_name, default_value):
    try:
        param_value = request.GET[param_name]
    except: 
        param_value = default_value
    
    return param_value
def get_post_values(request, param_name, default_value):
    try:
        param_value = request.POST[param_name]
    except: 
        param_value = default_value
        
    
    return param_value
def get_delete_values(request, param_name, default_value):
    try:
        param_value = request.DELETE[param_name]
    except: 
        param_value = default_value
        
    
    return param_value
def get_parameter_from_request(request, parameter_name, default_value, validTypes, islistBoolean = False):
    try:
        if(islistBoolean):
            parameterList = request.GET.getlist(parameter_name)
            if(len(parameterList) > 0):
                result_parameter=[]
                for parameter in parameterList:
                    result_parameter.append(get_value_by_type_and_default_value(parameter, default_value, validTypes))
            else:
                result_parameter = None
                
        else:
            parameter = request.GET[parameter_name]
            result_parameter = get_value_by_type_and_default_value(parameter, default_value, validTypes)

        
    except KeyError:
        return default_value
    
    return result_parameter


def get_value_by_type_and_default_value(parameter, default_value, validTypes):

    count = validTypes.count(type('str').__name__) + validTypes.count(type('unicode').__name__)

    if(count <= 0):
        parameter = convert_str_to_int(parameter)
       
    try:
        validTypes.index(type(parameter).__name__)
    except ValueError:
        return default_value

    return parameter

def get_random_id():
    return int(time.time()) + random.randint(0,900000000)