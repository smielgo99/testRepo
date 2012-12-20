>>> from suds.client import Client
>>> client = Client("http://127.0.0.1:8000/hello_world/service.wsdl", cache=None, faults=False)
>>> response = client.service.hello_world(hello_string="hei")
>>> print response
