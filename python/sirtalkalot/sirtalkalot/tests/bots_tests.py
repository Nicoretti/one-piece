#!/usr/bin/env python3
#
# Copyright (c) 2015, Nicola Coretti
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
import unittest
from unittest.mock import MagicMock
from sirtalkalot.bots import SlackBot


class SlackBotTests(unittest.TestCase):

    def setUp(self):
        self._auth_token = 'xoxo-Some-Auth-Token-8877'
        self._ws_handler = MagicMock()
        self._slackapi_backend = MagicMock()
        self.slackbot = SlackBot(self._auth_token, self._ws_handler)

    def test_if_registered_event_handlers_will_be_called_on_event(self):
        handler = MagicMock()
        self.slackbot.register('message', handler)
        self.slackbot._dispatch_event('message', {'text': 'stuff'})
        self.assertTrue(handler.called)

    def test_if_default_handler_is_called_if_no_handler_is_registered(self):
        default_handler = MagicMock()
        self.slackbot._default_handler = default_handler
        self.slackbot._dispatch_event('message', {'text': 'stuff'})
        self.assertTrue(default_handler.called)

    def test_slackbot_is_able_to_connect_to_slack_rmt_service(self):
        pass


if __name__ == '__main__':
    unittest.main()
