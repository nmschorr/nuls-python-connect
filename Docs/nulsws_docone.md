#The Nulsws-Python-Connect Libraries
##### by Nancy M Schorr, for Nuls-io
##### December, 2019
 
* Style Note: 
Please note: much of "correct" Python style is in lower case. Much of this code - being
 in an early dev stage does not yet follow these conventions, although it is my intent 
 for the finished product to follow them as much as possible. The coding style
 recommendation can be found here:  
 https://www.python.org/dev/peps/pep-0008/#package-and-module-names

### Introduction
The nulsws-python-connect library is built to provide communication between Nulstar ports and 
client applications and ports. It is based on the python library and framework 
__Tornado__.

Berzeck in Bolivia has been my mentor and lead on this project. The project goal is to 
implement the goals set forth mainly in these two Nulstar messaging documents: 

- Nulstar - Documentation - Module Specification.pdf
- Nulstar - Documentation - Message Protocol


These outline 8 types of JSON message structures to be supported initially. 4 are for 
the sending client, and 4 for the receiving/responding server. These libraries are the
 upon which Nuls customers can base their own Python-based modules messaging modules.

The eight types of messages in development are:
- 1  Negotiate Connection
- 2  Negotiate Connection Response
- 3  Request
- 4  Unsubscribe
- 5  Response
- 6  Ack
- 7  Register Compound Method
- 8  Unregister Compound Method.

 Messages have a common structure composed of six fields which comprise what I later 
 refer to as the "top" portion of the message:
-  ProtocolVersion: version the service to understand,2 numbers, major/minor
-  MessageID: identifies a request.
-  Timestamp:  Number  of  seconds  since  epoch January 1,1970
-  TimeZone: The time zone where the request was originated
-  MessageType: The message type, these are specified on section 3
-  MessageData: A Json object with the message payload

The first message sent from a client to the server is the request for a connection. 
Tornado takes care of all the necessary header details, including the request to 
"upgrade" the socket communication to http. 

 the first object that should be sent - only if the negotiation is ok service may process
 further requests -otherwise a NegotiateConnectionResponse object should be received with
 Status set to 0 (Failure) and disconnect immediately.

 "MessageType": "NegotiateConnection",
 "MessageData": {
     "CompressionAlgorithm": "zlib",
     "CompressionRate": "3"



## Tornado
 
Tornado is a Python a framework and asynchronous networking library, originally developed at FriendFeed - 
later acquired by Facebook. By using non-blocking network I/O, Tornado can scale to tens of 
thousands of open connections, making it ideal for long polling, WebSockets, and other applications that require a  
long-lived connection to each user.

WebSockets http://dev.w3.org/html5/websockets/,  The module implements the final version of the WebSocket protocol as
defined in `RFC 6455 <http://tools.ietf.org/html/rfc6455>`_. 

 Tornado 
is a scalable, non-blocking web server and web application framework written in Python.
 It provides a means for bidirectional communication between client and server.  It was
  developed by FriendFeed (acquired by Facebook in 2009), and was open-sourced soon 
  after. I chose this library after trying a few other that either weren't sufficiently
   supported and up-to-date, or were too complex for our needs.  Tornado does a 
   very satifactory job of setting up the ports for websocket bidirectional communication.
   The first communication between the ports is a little tricky. 
    The  header and preliminary messages look like this: The protocol has two parts:  a 
    handshake and the data transfer.

   The handshake from the client looks roughly like this:

        GET /chat HTTP/1.1
        Host: server.example.com
        Upgrade: websocket
        Connection: Upgrade
        Origin: http://example.com
        Sec-WebSocket-Protocol: chat, superchat
        Sec-WebSocket-Version: 13

   And the handshake from the server looks like::

        HTTP/1.1 101 Switching Protocols
        Upgrade: websocket
        Connection: Upgrade
        Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
        Sec-WebSocket-Protocol: chat
        
Once the client and server have done their handshakes - if successful -  data transfer 
 begins. This is a two-way communication where each side can, independently from the  
 other, send data.

### The nulsws-python-connect library contains the following files:

1) The Client, (ClientApp\nulsws_RUNNER_client.py) later to become both a client and a server.  The client 
uses the libraries to build JSON messages, then send them out, and receive the responses to those messages.

The main class is called NulsWebsocket. It uses Python's newer asyncio communication model. 

The four methods currently in nulsws_RUNNER are:

-  main(self, runlist, msg_type=3):  This method takes input from the scripting area below the class in the
 class file - ie, the runlist and the message type. Currently the message default is set to 3. The 
 development phase is focussed mainly on type 3. main() sets things in motion by executing  asyncio_run 
 which is the parent of all further asyncio activity in the client application.
 
 The runlist is a list of requests desired by the client - and to be answered by the Nulstar modules.
 
 main() first calls prep_NEGOTIATE_request() to prepare the top-to-middle portion of the JSON request.
 
Then main() calls:
  asyncio_run(  self.negotiate_list(   top_pls_middle_dict, myindx, runlist, mtpe))   
  
 sending it the top-to-middle portion, an indexing parameter to ensure no two requests have the same id, 
 the requesting "runlist" of api requests, and the message type which in this case is '3' for request.
  
 main() then calls "negotiate list". This method set's up the connection with the target port, then sends 
 message type 2 which is a Negotiate request. This negotiation must be done every time a port is opened.
 
 After the opening and negotiating, the "Regular" request is sent via:
  REGULAR_req(self, websock_connct: WebSocketClientConnection, j_reg_dict):
 
 The 'connection' is sent to this method with the "Regular" request.
 
The runlist is put at the bottom of the main client file like this:

'''
if __name__ == '__main__':
    RUNLIST = [b.AC_GET_ACCOUNT_BYADDRESS, b.AC_GET_ALL_ADDRESS_PREFIX, b.AC_GET_ACCOUNT_LIST,
                b.AC_GET_ADDRESS_LIST, b.AC_GET_ADDRESS_PREFIX_BY_CHAINID, b.AC_GET_ALL_ADDRESS_PREFIX,
                b.AC_GET_ALL_PRIKEY, b.AC_GET_ALIASBY_ADDRESS]
    message_type = 3 
    nws = NulsWebsocket()    
    nws.main(RUN_LIST, message_type)
'''

The framework then include a set of Constants libraries. This is a somewhat complex 
behind-the-scenes mechanism that make setting preferences for each of the 228 or so 
types of message easy for the developer.  Within those 228 types of requests are 124 
different parameters. Many of the requests only require one or parameters, but some as 
many as eight or so. With the average being maybe 3-4 - that gives us a total of around
1,000 possible specific parameters for this nuls-python-connect library.

The user/developer initially only needs to set parameter for those functions he/she is 
interested in. The settings go into two user parameter files in the UserSettings 
directory. 

The first file, nulsws-USER_PARAMS.py, contains every one of the possible parameters. 
Once set in this file, it is fed into the library, and no further setup is needed to 
access the as-is nuls blockchain via the Nulstar Connector module. 

Here's a sample 