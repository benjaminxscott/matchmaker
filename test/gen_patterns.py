#!/usr/bin/env python
# Create sample STIX file to test matcher
# Success = all "patterns" within Indicators match at least one "instance" within Observables 

from stix.indicator import Indicator, CompositeIndicatorExpression

from stix.core import STIXPackage, STIXHeader
from cybox.common import Hash
import cybox.utils

from cybox.core import ObservableComposition

from cybox.objects.email_message_object import EmailMessage,Attachments,AttachmentReference
from cybox.objects.socket_address_object import SocketAddress
from cybox.objects.port_object import Port
from cybox.objects.domain_name_object import DomainName
from cybox.objects.file_object import File
from cybox.objects.mutex_object import Mutex
from cybox.objects.http_session_object import *
from cybox.objects.win_registry_key_object import *

# setup header
pkg = STIXPackage()
stix_header = STIXHeader()
stix_header.title = "Indicators"
stix_header.add_package_intent ("Indicators")

pkg.stix_header = stix_header

# -- IP INSTANCE--
obj = SocketAddress()
obj.ip_address =  '1.2.3.4'
pkg.add_observable(obj)


# -- IP INDICATOR --
ind = Indicator()
ind.title = "IP address pattern"

ind.add_indicator_type( "IP Watchlist")
ind_obj = SocketAddress()
ind_obj.ip_address =  '1.2.3.4'
ind_obj.ip_address.condition= "Equals"
port = Port()
port.port_value = '1337'
port.port_value.condition= "Equals"
ind_obj.port = port

ind.add_object(ind_obj)
pkg.add_indicator(ind)

# -- DOMAIN INSTANCE --
obj = DomainName()
obj.value = 'evil.com'
pkg.add_observable(obj)


# -- DOMAIN INDICATOR --
ind = Indicator()
ind.add_indicator_type ("Domain Watchlist")
ind.title = "Domain pattern"

ind_obj = DomainName()
ind_obj.value = 'evil.com'
ind_obj.value.condition= "Equals"
ind.add_object(ind_obj)
pkg.add_indicator(ind)


# -- FILE INSTANCE --

obj = File()
obj.file_name = "evil.exe"
digest = Hash()
digest.simple_hash_value = "7c2ac20e179fc78f71b2aa93c744f4765ea32e30403784beaef58f20ed015be5"

obj.add_hash(digest)
pkg.add_observable(obj)

# -- FILE INDICATOR --

ind = Indicator()
ind.title = "File pattern"
ind.add_indicator_type ("File Hash Watchlist")

ind_obj = File()
ind_obj.file_name = "evil.exe"
ind_obj.file_name.condition = "Equals"
digest = Hash()
digest.simple_hash_value = "7c2ac20e179fc78f71b2aa93c744f4765ea32e30403784beaef58f20ed015be5"
digest.simple_hash_value.condition = "Equals"
digest.type_.condition = "Equals"

ind_obj.add_hash(digest)
ind.add_object(ind_obj)
pkg.add_indicator(ind)

# -- COMPOSITION of two file objects --
comp = ObservableComposition()
comp.operator = "OR"
comp.add(ind_obj) # re-use file object

other_obj = File()
other_obj.file_name = "nohash.exe"
other_obj.file_name.condition = "Equals"
comp.add(other_obj)

pkg.add_observable(comp)


# -- COMPOSITION of two indicators --
indcomp = Indicator() 
indcomp.composite_indicator_expression = CompositeIndicatorExpression()
indcomp.composite_indicator_expression.operator = "OR"

indcomp.composite_indicator_expression.append(ind) #re-use file indicator
indcomp.composite_indicator_expression.append(ind)

pkg.add_indicator(indcomp)

# -- EMAIL INSTANCE --
file_obj = obj # re-use File from above

obj = EmailMessage()
obj.subject = "Buy Pharma Now Reference 1badd00d"
obj.sender = "spammer@site.ru"

obj.add_related(file_obj, "Contains") 
attach = Attachments()
attach.append(file_obj.parent.id_)

obj.attachments = attach

pkg.add_observable(obj)

# -- EMAIL INDICATOR --
file_ind_obj = ind_obj # re-use File pattern from above
ind = Indicator()
ind.title = "Email pattern"
ind.add_indicator_type ("Malicious E-mail")
ind_obj = EmailMessage()
ind_obj.subject = "Buy Pharma Now"
ind_obj.subject.condition= "Contains"
ind_obj.sender = "spammer@site.ru"
ind_obj.sender.condition= "Equals"


ind_obj.add_related(file_ind_obj, "Contains") 
attach = Attachments()
attach.append(file_ind_obj.parent.id_)

ind_obj.attachments = attach
ind.add_object(ind_obj)

pkg.add_indicator(ind)
    
# -- USER AGENT INSTANCE --
fields = HTTPRequestHeaderFields()
fields.user_agent = "lynx 3.0"

header = HTTPRequestHeader()
header.parsed_header = fields

request = HTTPRequestResponse()
request.http_client_request = HTTPClientRequest()
request.http_client_request.http_request_header = header

obj = HTTPSession()
obj.http_request_response = [request]
pkg.add_observable(obj)

# -- USER AGENT INDICATOR --

ind = Indicator()
ind.title = "User Agent pattern"
ind.add_indicator_type ("C2")
ind_header = HTTPRequestHeader()
ind_header.parsed_header = fields

ind_fields = HTTPRequestHeaderFields()
ind_fields.user_agent = 'lynx'
ind_fields.user_agent.condition = "Contains"
ind_header.parsed_header = ind_fields

ind_request = HTTPRequestResponse()
ind_request.http_client_request = HTTPClientRequest()
ind_request.http_client_request.http_request_header = ind_header

ind_obj = HTTPSession()
ind_obj.http_request_response = [ind_request]
ind.add_object(ind_obj)
pkg.add_indicator(ind)


# -- URI INSTANCE --

response = HTTPRequestResponse()
response.http_client_request = HTTPClientRequest()
response.http_client_request.http_request_line = HTTPRequestLine()
response.http_client_request.http_request_line.http_method = 'GET'
response.http_client_request.http_request_line.value = '/gate.php'


obj = HTTPSession()
obj.http_request_response = [response]
pkg.add_observable(obj)

# -- URI INDICATOR --
ind = Indicator()

ind.title = "URI pattern"
ind.add_indicator_type ("URL Watchlist")
ind_response = HTTPRequestResponse()
ind_response.http_client_request = HTTPClientRequest()
ind_response.http_client_request.http_request_line = HTTPRequestLine()
ind_response.http_client_request.http_request_line.http_method = 'GET'
ind_response.http_client_request.http_request_line.value = '/gate.php'

ind_response.http_client_request.http_request_line.http_method.condition = "Equals" 
ind_response.http_client_request.http_request_line.value.condition = "Equals" 


ind_obj = HTTPSession()
ind_obj.http_request_response = [ind_response]
ind.add_object(ind_obj)
pkg.add_indicator(ind)



# -- REGISTRY INSTANCE --
obj = WinRegistryKey()
keys = RegistryValues()
key = RegistryValue()
key.name = 'HLKM\STARTUP'
key.data = "BADFILE.exe"
keys.append(key)
obj.values = keys

pkg.add_observable(obj)

# -- REGISTRY INDICATOR --
ind = Indicator()
ind.title = "Registry pattern"
ind.add_indicator_type ("Host Characteristics")
ind_obj = WinRegistryKey()
ind_keys = RegistryValues()
ind_key = RegistryValue()

ind_key.name = 'HLKM\STARTUP'
ind_key.name.condition = "Equals"
ind_key.data = "BADFILE"
ind_key.data.condition = "Contains"

ind_keys = RegistryValues()
ind_keys.append(ind_key)
ind_obj.values = ind_keys
ind.add_object(ind_obj)
pkg.add_indicator(ind)

# -- MUTEX INSTANCE --
obj = Mutex()
obj.name = "heymanitsme"

pkg.add_observable(obj)


# -- MUTEX INDICATOR --
ind = Indicator()
ind.title = "Mutex pattern" 
ind.add_indicator_type ("Host Characteristics")
ind_obj = Mutex()
ind_obj.name = "heyman"
ind_obj.name.condition= "Contains"
ind.add_object(ind_obj)
pkg.add_indicator(ind)

print pkg.to_xml() 
