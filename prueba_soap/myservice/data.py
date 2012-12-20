# -*- coding: utf-8 -*-
from soaplib.serializers.clazz import Array, ClassSerializer
from soaplib.serializers.primitive import String, Integer

class Permission(ClassSerializer):
    application = String
    feature = String


