
####/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect
# import tornado
# import tornado.platform
from tornado import escape


class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.ws = None
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.connect1()
        PeriodicCallback(self.keep_alive2, 20000).start()
        self.ioloop.start()

    @gen.coroutine
    def connect1(self):
        print("trying to connect")
        try:
            self.ws = yield websocket_connect(self.url)
        except Exception as e:
            print("connection error")
        else:
            print("connected")

            self.run3()


    def keep_alive2(self):
        if self.ws is None:
            self.connect1()
        else:
            self.ws.write_message("keep alive")


    @gen.coroutine
    def run3(self):
        # send_this = '\{ \'POST  HTTP/1.1', 'Host: 127.0.0.1:18003', 'Content-Type: application/json;charset=UTF-8', 'Accept: */*', 'Cache-Control: no-cache' ,'Host: 127.0.0.1:18003', 'Accept-Encoding: gzip deflate' ,'Content-Length: 80' ,'Connection: keep-alive', 'cache-control: no-cache', 'jsonrpc: 2.0' , 'method : getChainInfo',  'params:[]', 'id: 1234' \}'
        send_this = "{ 'POST  HTTP/1.1', 'Host: 127.0.0.1:18003', 'Content-Type: application/json;charset=UTF-8', 'Accept: */*', 'Cache-Control: no-cache' ,'Host: 127.0.0.1:18003', 'Accept-Encoding: gzip deflate' ,'Content-Length: 80' ,'Connection: keep-alive', 'cache-control: no-cache', 'jsonrpc: 2.0' , 'method : getChainInfo',  'params:[]', 'id: 1234' }"
        json_str = escape.json_encode(send_this)
        while True:
            msg = yield self.ws.read_message()
            if msg is None:
                print("connection closed")
                self.ws = None
                #break
            else:
                yield self.ws.write_message("hello1")
                yield self.ws.write_message(json_str)
                res = yield self.ws.read_message()
                self.assertEqual(res, "hello1")
                res = yield self.ws.read_message()
                self.assertEqual(res, json_str)


if __name__ == "__main__":
    method : str = "ws://"
    host = "localhost"
    port = "9006"
    #port = "18003"
    uri : str = ''.join([method, host, ":", port])
    print(" uri:  ", uri)
    client = Client(uri, 5)

# send_this = '\{ \'POST  HTTP/1.1', 'Host: 127.0.0.1:18003', 'Content-Type: application/json;charset=UTF-8', 'Accept: */*', 'Cache-Control: no-cache' ,'Host: 127.0.0.1:18003', 'Accept-Encoding: gzip deflate' ,'Content-Length: 80' ,'Connection: keep-alive', 'cache-control: no-cache', 'jsonrpc: 2.0' , 'method : getChainInfo',  'params:[]', 'id: 1234' \}'
























# import json
# import asyncio
# from tornado import platform.
#
#
# # OPCODE=TEXT, FIN=0, MSG="Too much "
# from websocket.tests.test_websocket import TRACEABLE
#
#
# class n_socket(object):
#
#     def __init__(self):
#         ws.enableTrace(TRACEABLE)
#
#         self.url: str = "ws://127.0.0.1:7771"
#
#         sock = ws.WebSocket()
#         sock.set_mask_key(_abnf.create_mask_key)
#         self.data = {
#             "MessageID": "45sdj8jcf8899ekffEFefee",
#             "Timestamp": "1542102459",
#             "TimeZone": "-8",
#             "MessageType": "Request",
#             "MessageData": {
#                 "SubscriptionEventCounter": "3",
#                 "SubscriptionPeriod": "0",
#                 "SubscriptionRange": "0",
#                 "ResponseMaxSize": "0",
#                 "RequestMethods": [
#                     {
#                     "GetBalance": {
#                         "Address": "tNULSeBaMnrs6JKrCy6TQdzYJZkMZJDng7QAsD"
#                     }
#                     }
#                 ]
#                 }
#             }
#
#         self.sock = sock
#
#
#     async def main(self):
#         ws_conn = self.sock.create_connection(self.url)
#
#         frame = ABNF.create_frame(self.data, OPCODE='TEXT', fin=0)
#
#         print("Sending json query frame ...")
#
#         ws_conn.send_frame(frame)
#         await ws_conn.recv_data()
#
# n = n_socket()
# asyncio.get_event_loop().run_until_complete(n.main())
#













# hs = ws_conn.handshake_response

# payload_test: str = "hello"
# data_dict: dict = {
#     "MessageType": "Request",
#     "MessageData":
#         {"jsonrpc": "2.0",
#          "method": "getChainInfo",
#          "params": [],
#          "id": 1234
#          }
# }



# "TimeZone", "MessageID", "Timestamp", "MessageType", "MessageData"
# payload = bytes(jsond, 'utf-8')
# ws_conn.getstatus()
# ws_conn.getheaders()
# # ws_conn.send(payload, websocket.ABNF.OPCODE_TEXT)
# jsond = json.dumps(self.data2)

# ws_conn.send(payload, websocket.ABNF.OPCODE_TEXT)
#
# print("Waiting for json query...")
#
# resultb = ws_conn.recv()
#
# print("Result from json query: ", resultb)

# ws.close()
#
