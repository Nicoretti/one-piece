#!/usr/bin/env python3
#
# Copyright (c) 2014, Nicola Coretti
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import logging
from queue import Queue

from ws4py.client.threadedclient import WebSocketClient

__version__ = "0.0.1"
__author__ = 'Nicola Coretti'
__email_ = 'nico.coretti@gmail.com'


class BasicWebSocketHandler(WebSocketClient):

    def __init__(self):
        self._ws_client = None
        self._message_received_listeners = []
        self._input_queue = Queue()
        self._output_queue = Queue()

    @property
    def input_queue(self):
        return self._input_queue

    def send(self, message):
        super().send(message)

    def connect(self, url):
        super().__init__(url)
        super().connect()
        super().run_forever()

    def close(self):
        self._sender_thread.join()
        self._ws_client.close(1000, 'Close Reason')

    def opened(self):
        logging.info('connected to slack')

    def closed(self, code, reason):
        logging.info('disconnected to slack')

    def received_message(self, message):
        logging.debug('message received: {0}'.format(message))
        self.cb(message)
        self._input_queue.put(message)
