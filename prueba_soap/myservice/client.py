# This program is free software; you can redistribute it and/or modify
# it under the terms of the (LGPL) GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the 
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library Lesser General Public License for more details at
# ( http://www.gnu.org/licenses/lgpl.html ).
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# written by: Jeff Ortel ( jortel@redhat.com )

import sys
sys.path.append('../')

import logging
import traceback as tb
import suds.metrics as metrics
from tests import *
from suds import WebFault
from suds.client import Client

errors = 0

setup_logging()

#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.metrics').setLevel(logging.DEBUG)
#logging.getLogger('suds').setLevel(logging.DEBUG)


def start(url):
    global errors
    print '\n________________________________________________________________\n' 
    print 'Test @ ( %s ) %d' % (url, errors)

try:
    url = 'http://mssoapinterop.org/asmx/simple.asmx?WSDL'
    start(url)
    client = Client(url)
    print client
    # string
    input = "42"
    d = dict(inputString=input)
    result = client.service.echoString(**d)
    print 'echoString() =  %s' % result
    assert result == input
    # int
    input = 42
    result = client.service.echoInteger(input)
    print 'echoInteger() = %s' % result
    assert result == input
    # float
    input = 4.2
    result = client.service.echoFloat(input)
    print 'echoFloat() = %s' % result
    assert result == input
    # suds 0.3.8+
    result = client.service.echoIntegerArray([])
    print 'echoIntegerArray() = %s' % result
    assert result is None
    input = [1,2,3,4]
    result = client.service.echoIntegerArray(input)
    print 'echoIntegerArray() = %s' % result
    assert result == input
    result = client.service.echoIntegerArray(inputIntegerArray=input)
    print 'echoIntegerArray() = %s' % result
    assert result == input
except WebFault, f:
    errors += 1
    print f
    print f.fault
except Exception, e: 
    errors += 1
    print e
    tb.print_exc()
    
try:
    url = 'http://127.0.0.1:8000/hello_world/service.wsdl'
    start(url)
    client = Client(url)
    print client
    result = client.service.Test('1','2')
    print 'echoInteger() = %s' % result
    assert result == input
except WebFault, f:
    errors += 1
    print f
    print f.fault
except Exception, e: 
    errors += 1
    print e
    tb.print_exc()
    


print '\nFinished: errors = %d' % errors
