#!/usr/bin/env python

#
#The MIT License (MIT)
#
#Copyright (c) 2016 Mario Romero 
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import json
import websocket
from models import StreamUpdate


class Listener(object):
    def on_connect(self):
        pass

    def on_update(self, json_data):
        pass

    def on_close(self, **kwargs):
        pass



class Client(object):
    def __init__(self, listener):
        self.listener = listener
        self._ws_url = 'wss://ws.bitso.com'
        self.ws_client = websocket.WebSocketApp(self._ws_url,
                            on_message = self._on_message,
                            on_error = self._on_error,
                            on_close = self._on_close)
        self.channels = []
        self.book = None

    def connect(self, channels, book):
        self.channels = channels
        self.book = book
        self.ws_client.on_open = self._on_open
        self.ws_client.run_forever()

    def close(self):
        print "received close"
        self.ws_client.close()

    def _on_close(self, ws):
        print "closing connection"
        self.listener.on_close()
        
    def _on_error(self, ws, error):
        print error
        
    def _on_open(self, ws):
        for channel in self.channels:
            self.ws_client.send(json.dumps({ 'action': 'subscribe', 'book': self.book, 'type': channel }))
        self.listener.on_connect()

    def _on_message(self, ws, m):
        val = json.loads(m)
        obj = StreamUpdate(val)
        self.listener.on_update(obj)
        
        
    
