#!usr/bin/python3.7

# Messages have a common structure composed of six fields:
# •  ProtocolVersion: version the service to understand,2 numbers, major/minor
# •  MessageID: identifies a request.
# •  Timestamp:  Number  of  seconds  since  epoch January 1,1970
# •  TimeZone: The time zone where the request was originated
# •  MessageType: The message type, these are specified on section 3
# •  MessageData: A Json object with the message payload

# the first object that should be sent - only if the negotiation is ok service may process
# further requests -otherwise a NegotiateConnectionResponse object should be received with
# Status set to 0 (Failure) and disconnect immediately.

# "MessageType": "NegotiateConnection",
# "MessageData": {
#     "CompressionAlgorithm": "zlib",
#     "CompressionRate": "3"

## -- Enter your custom settings data via the library file nulsuserone.py
# Note: Don't use typing.Dict - it can cause json problems when converted
# This file right now is the client only.
# author:  Nancy M Schorr, for Nuls
# December 2, 2019


from asyncio import run as asyncio_run
from asyncio import sleep as asyncio_sleep
from tornado.websocket import websocket_connect  # WebSocketClosedError
from tornado.websocket import WebSocketClientConnection
from nulsws_library import *
from nulsws_usersets_negt_type1 import websock_url_negt

class NulsWebsocket(object):
    def __init__(self):
        myprint("the url:  ", websock_url_negt)
        self.mindex = 0

    def nms_callback(self, x):
        print(x)

    async def REGISTER_REQ(self, connct: WebSocketClientConnection, regis_msg):
        json_prt(regis_msg, "* * * _REGISTER_ message going out: ")
        await connct.write_message(regis_msg)      # 2 WRITE
        await asyncio_sleep(3)
        read_msg_a = await connct.read_message(self.nms_callback("msg just recieved"))  # 3 READ
        await asyncio_sleep(2)
        if len(read_msg_a ) > 10:
            json_prt(read_msg_a, "-------! ! ! _REGISTER_ response received: ")
        print("-----------end _REGISTER_-----------------------------------")

    async def REGULAR_req(self, websock_connct: WebSocketClientConnection, json_REG):
        json_prt(json_REG, "* * * REGULAR message going out: ")
        myprint("* * * Sending Regular request going out:")
        await websock_connct.write_message(json_REG)      # 2 WRITE
        await asyncio_sleep(2)
        read_REG= await websock_connct.read_message(self.nms_callback(""))  # 3 READ
        await asyncio_sleep(2)
        if len(read_REG) > 10:
            json_prt(read_REG, "-------! ! ! REGULAR response received: ")
        print("--------------end Regular request--------------------------------")

    async def negotiate(self, json_negotiate, jreg, jmain):
        connection = await websocket_connect(websock_url_negt)   # 1) CONNECT
        await asyncio_sleep(3)
        while (not connection):
            await asyncio_sleep(1)
        json_prt(json_negotiate, "* * * First message going out- Negotiate: ")
        await connection.write_message(json_negotiate) # 2) WRITE
        await asyncio_sleep(3)

        negotiate_res_MSG = await connection.read_message()    # 3 READ
        await asyncio_sleep(2)
        json_prt(negotiate_res_MSG, "! ! ! Negotiate response is this: ")
        print("------end Negotiate----------------------------------------")
        await self.REGISTER_REQ(connection, jreg)
        await self.REGULAR_req(connection, jmain)

    def commander(self, jconnect, json_register, json_main_type):
        asyncio_run(self.negotiate(jconnect, json_register, json_main_type))   # starts event loop

    def main(self, mtpe):
        # we always do type 1 just before anything
        import nulsws_msgs_others as mw
        from nulsws_msgtype_register import make_nulsws_REGISTER_method
        self.mindex += 1
        mind = self.mindex
        json_main_type = None

        json_negotiate = mw.prep_NEGOTIATE_data_type1(mind)
        json_register =  make_nulsws_REGISTER_method(mind)

        if mtpe == 3:
            json_main_type = mw.prep_data_REQUEST_type3(mind)
        if mtpe == 5:
            pass
            # json_main_type = mw.prep_data_REQUEST_type5()
        if mtpe == 7:
            pass
            # json_main_type = mw.prep_data_REQUEST_type7()


        self.commander(json_negotiate, json_register, json_main_type)


if __name__ == '__main__':
    mtype = 3                       # either 3, 5, or 7, or 99 for r
    n = NulsWebsocket()
    n.main(mtype)


## -- enter user data via the library file nulsws_msgtype<1,2,3>.py


