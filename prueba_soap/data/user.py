# -*- coding: utf-8 -*-
from soaplib.serializers.clazz import Array, ClassSerializer
from soaplib.serializers.primitive import String, Integer

'''
This is a simple HelloWorld example to show the basics of writing
a webservice using soaplib, starting a server, and creating a service
client.
'''


class Permission(ClassSerializer):
    application = String
    feature = String





