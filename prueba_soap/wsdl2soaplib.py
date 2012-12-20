from StringIO import StringIO

import os.path
import sys
import textwrap
import keyword
import re

import suds.client

VALID_IDENTIFIER_RE                   = re.compile(r'[_A-Za-z][_A-Za-z1-9]*')
VALID_IDENTIFIER_FIRST_LETTER_RE      = re.compile(r"[_A-Za-z]")
VALID_IDENTIFIER_SUBSEQUENT_LETTER_RE = re.compile(r"[_A-Za-z1-9]")

HEADER = '''\
"""SOAP web services generated from:
%(wsdl)s.
"""

from soaplib.serializers.primitive import (
        String, Integer, Float, Double, DateTime, Bolean, Null, Array, Map, Any
    )
from soaplib.serializers.clazz import ClassSerializer

from soaplib.service import SoapServiceBase
from soaplib.service import soapmethod
'''

INTERFACE = '''\
class %(name)s(%(bases)s):
    """%(docstring)s"""
'''

SERVICE_INTERFACE_DOCSTRING = '''\
SOAP service ``%(serviceName)s`` with target namespace %(tns)s.
'''

TYPE_INTERFACE_DOCSTRING = '''\
SOAP %(type)s ``{%(namespace)s}%(name)s``
'''

TYPE_MAP = '''\
WSDL_TYPES = {
%(items)s
}
'''

SOAPMETHOD = '''    @soapmethod(%(args)s, _returns=%(response)s)'''

METHOD = '''    def %(name)s(self, %(args)s):'''

METHOD_DOCSTRING = '''\
        """Parameters:

        %(args)s

        Returns: %(response)s
        """
'''

STANDARD_TYPE_NAMESPACES = [
    'http://schemas.xmlsoap.org/soap/encoding/',
    'http://schemas.xmlsoap.org/wsdl/',
    'http://www.w3.org/2001/XMLSchema'
]

SCHEMA_TYPE_MAPPING = {
    None:                   '%(typeName)s',

    'None':                 'None',

    'boolean':              'Boolean',
    'string':               'String',

    'long':                 'Integer',
    'int':                  'Integer',
    'short':                'Integer',
    'byte':                 'Integer',

    'unsignedLong':         'Integer',
    'unsignedInt':          'Integer',
    'unsignedShort':        'Integer',
    'unsignedByte':         'Integer',

    'positiveInteger':      'Integer',
    'nonPositiveInteger':   'Integer',
    'negativeInteger':      'Integer',
    'nonNegativeInteger':   'Integer',

    'float':                'Float',
    'double':               'Float',

    'decimal':              'Decimal',

    'dateTime':             'DateTime',
    'date':                 'DateTime',

    'anyURI':               'String',
    'token':                'String',
    'normalizedString':     'String',

    'base64Binary':         'String',
    'hexBinary':            'String',
}

def formatDocstring(text, indent=4, colwidth=78):
    width = colwidth - indent
    joiner = '\n' + ' ' * indent
    return joiner.join(textwrap.wrap(text, width) + [''])

def typeName(type, sd):
    resolved = type.resolve()
    return resolved.name or ''

def schemaTypeName(type, sd, deps=None):

    resolved = type.resolve()
    name = resolved.name or ''

    schemaType = SCHEMA_TYPE_MAPPING.get(name)
    if schemaType is None: # not a standard type

        # user default
        schemaType = SCHEMA_TYPE_MAPPING[None] 

        # possibly save dependency link
        if deps is not None:
            deps.append(unicode(name))

    required = type.required()
    schemaType = schemaType % dict(typeName=name, required=required)

    if type.unbounded():
        schemaType = "Array(%s)" % schemaType

    return schemaType

def normalizeIdentifier(identifier):
    if not VALID_IDENTIFIER_RE.match(identifier):
        newIdentifierLetters = []
        firstLetter = True
        for letter in identifier:
            if firstLetter:
                if VALID_IDENTIFIER_FIRST_LETTER_RE.match(letter):
                    newIdentifierLetters.append(letter)
                else:
                    newIdentifierLetters.append('_')
                firstLetter = False
            else:
                if VALID_IDENTIFIER_SUBSEQUENT_LETTER_RE.match(letter):
                    newIdentifierLetters.append(letter)
                else:
                    newIdentifierLetters.append('_')
        identifier = ''.join(newIdentifierLetters)

    if keyword.iskeyword(identifier):
        identifier = identifier + '_'

    return identifier

def generate(client, url=None, standardTypeNamespaces=STANDARD_TYPE_NAMESPACES, removeInputOutputMesssages=True):
    """Given a WSDL URL, return a file that could become your interfaces.py
    """

    printed = [] # sequence of type name -> string

    for sd in client.sd:

        serviceOut = StringIO()

        print >>serviceOut, HEADER % dict(
                wsdl=url,
            )

        printed.append(('', serviceOut.getvalue(),))

        # Types

        typeMap = {}
        typeSeq = []
        typeDeps = {}
        typeAttributes = {}

        typesPrinted = []

        for type_ in sd.types:

            typeOut = StringIO()

            resolved = type_[0].resolve()
            namespaceURL = resolved.namespace()[1]
            if namespaceURL not in standardTypeNamespaces:

                if resolved.enum():
                    typeDescription = "enumeration"
                else:
                    typeDescription = "complex type"

                # Look for basess
                interfaceBases = []
                if resolved.extension():
                    def find(t):
                        for c in t.rawchildren:
                            if c.extension():
                                find(c)
                            if c.ref is not None:
                                interfaceBases.append(c.ref[0])
                    find(resolved)

                if not interfaceBases:
                    interfaceBases = ['ClassSerializer']

                rawTypeName = typeName(type_[0], sd)

                typeInterfaceName = normalizeIdentifier(rawTypeName)

                typeMap[rawTypeName] = typeInterfaceName
                typeSeq.append((rawTypeName, typeInterfaceName,))
                typeAttributes[rawTypeName] = {}

                print >>typeOut, INTERFACE % dict(
                        name=normalizeIdentifier(typeInterfaceName),
                        bases=', '.join(interfaceBases),
                        docstring=formatDocstring(TYPE_INTERFACE_DOCSTRING % dict(
                                type=typeDescription,
                                name=rawTypeName,
                                namespace=namespaceURL,
                            )
                        )
                    )

                print >>typeOut, "    class types:"

                if resolved.enum():
                    for attr in type_[0].children():
                        name = attr[0].name.replace(' ', '_')
                        print >>typeOut, "        %s = String # XXX: Enumeration value" % name
                else:
                    for attr in type_[0].children():
                        name = attr[0].name.replace(' ', '_')
                        attrTypeName = typeName(attr[0], sd)
                        typeAttributes[rawTypeName][name] = attrTypeName
                        schemaType = schemaTypeName(attr[0], sd, deps=typeDeps.setdefault(unicode(rawTypeName), []))
                        print >>typeOut, "        %s = %s" % (normalizeIdentifier(name), schemaType,)

                print >>typeOut

                typesPrinted.append((rawTypeName, typeOut.getvalue(),))

        serviceInterfaceOut = StringIO()

        # Main service interface
        print >>serviceInterfaceOut, INTERFACE % dict(
                name=normalizeIdentifier(sd.service.name),
                bases=u"SoapServiceBase",
                docstring=formatDocstring(SERVICE_INTERFACE_DOCSTRING % dict(
                        serviceName=sd.service.name,
                        tns=sd.wsdl.tns[1],
                    )
                )
            )

        methods = {} # name -> (response type, list of parameters,)

        for p in sd.ports:
            for m in p[1]:
                methodName = m[0]
                methodArgs = m[1]
                if methodName not in methods:
                    methodDef = p[0].method(methodName)

                    # XXX: This is discards the namespace part
                    if methodDef.soap.output.body.wrapped:

                        inputMessage  = methodDef.soap.input.body.parts[0].element[0]
                        outputMessage = methodDef.soap.output.body.parts[0].element[0]

                        if outputMessage in typeAttributes:
                            if len(typeAttributes[outputMessage]) > 0:
                                response = typeAttributes[outputMessage].values()[0]
                            else:
                                response = "None"
                        else:
                            response = outputMessage

                        # Remove types used as input/output messages
                        if removeInputOutputMesssages:
                            remove = False
                            for idx, (t, x) in enumerate(typesPrinted):
                                if t == inputMessage:
                                    remove = True
                                    break
                            if remove:
                                del typesPrinted[idx]
                                if inputMessage in typeMap:
                                    del typeMap[inputMessage]

                            remove = False
                            for idx, (t, x) in enumerate(typesPrinted):
                                if t == outputMessage:
                                    remove = True
                                    break
                            if remove:
                                del typesPrinted[idx]
                                if outputMessage in typeMap:
                                    del typeMap[outputMessage]

                    else:
                        response = methodDef.soap.output.body.parts[0].element[0]

                    methods[methodName] = (response, methodArgs,)

        for methodName in sorted(methods):

            methodArgNames = [m[0] for m in methods[methodName][1]]
            methodReturnType = methods[methodName][0]

            methodArgDetails = []
            methodArgSpecs = []

            for m in methods[methodName][1]:
                argDetail = m[1]

                # for docstring

                methodModifierParts = []

                if not argDetail.required():
                    methodModifierParts.append('optional')
                if argDetail.nillable:
                    methodModifierParts.append('may be None')

                methodModifiers = ""
                if methodModifierParts:
                    methodModifiers = ' (%s)' % ', '.join(methodModifierParts)

                argTypeName = typeName(argDetail, sd)

                methodSpec = "``%s`` -- %s%s" % (
                        argDetail.name,
                        argTypeName,
                        methodModifiers
                    )

                methodArgDetails.append(methodSpec)

                # for @soapmethod decorator

                schemaType = schemaTypeName(argDetail, sd)
                methodArgSpecs.append(schemaType)

            # TODO: Probably not aware of array return types
            if methodReturnType not in typeMap and methodReturnType in SCHEMA_TYPE_MAPPING:
                methodReturnType = SCHEMA_TYPE_MAPPING[methodReturnType]

            print >>serviceInterfaceOut, SOAPMETHOD % dict(
                    args=', '.join(methodArgSpecs),
                    response=methodReturnType,
                )

            print >>serviceInterfaceOut, METHOD % dict(
                    name=normalizeIdentifier(methodName),
                    args=', '.join(methodArgNames),
                )

            print >>serviceInterfaceOut, METHOD_DOCSTRING % dict(
                    args='\n        '.join(methodArgDetails),
                    response=methodReturnType,
                )

            print >>serviceInterfaceOut

        # Sort list of complex types based on internal dependencies

        def sortDeps(printed):

            printed = list(reversed(printed))

            queue = [item for item in printed if len(typeDeps.get(unicode(item[0]), [])) == 0]
            satisfied = set(queue)
            remaining = [item for item in printed if item not in queue]

            sortedPrinted = []

            while queue:
                item = queue.pop()
                itemTypeName = unicode(item[0])

                sortedPrinted.append(item)
                satisfied.add(itemTypeName)

                for item in remaining:

                    remainingItemTypeName = unicode(item[0])

                    depsList = typeDeps.get(remainingItemTypeName, [])
                    remainingDeps = []
                    for dep in depsList:
                        if dep not in satisfied:
                            remainingDeps.append(dep)

                    typeDeps[remainingItemTypeName] = remainingDeps

                    if len(remainingDeps) == 0:
                        queue.append(item)
                        remaining.remove(item)

            return sortedPrinted

        typesPrinted = sortDeps(typesPrinted)

        # Print everything
        printed.extend(typesPrinted)
        printed.append((sd.service.name, serviceInterfaceOut.getvalue(),))

        typeMapOut = StringIO()
        print >>typeMapOut, TYPE_MAP % dict(
                items=',\n'.join(["    '%s': %s" % k for k in typeSeq if k[0] in typeMap])
            )
        print >>typeMapOut
        printed.append(('', typeMapOut.getvalue(),))

    return '\n'.join([v[1] for v in printed])

def main():
    if len(sys.argv) " % sys.argv[0]
        print "The output will be printed to the console"
        return

    if not '://' in sys.argv[1]:
        sys.argv[1] = 'file://' + os.path.abspath(sys.argv[1])

    client = suds.client.Client(sys.argv[1])
    print generate(client, sys.argv[1])

if __name__ == '__main__':
    main()
