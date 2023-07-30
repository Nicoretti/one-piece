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
import json
import logging
from collections import defaultdict

import pkg_resources
import docopt

from libslack.slackapi import SlackApi

from sirtalkalot import services
from sirtalkalot import websocket

__version__ = "0.0.1"
__author__ = 'Nicola Coretti'
__email_ = 'nico.coretti@gmail.com'


class SlackApiError(Exception):
    pass


class RtmError(Exception):
    pass


class SlackBot(object):
    """
    """

    def __init__(self, authentication_token, websocket_handler):
        """
        Creates a new SlackBot.

        :param string authentication_token: which will be used to authenticate against the slack api.
        :param websocket_handler: which will be used to connect and interact with the rtm webservice.
        """
        self._ws_client = websocket_handler()
        self._authentication_token = authentication_token
        self._slack_api = SlackApi(self._authentication_token)
        self._event_handlers = defaultdict(lambda: self._default_handler)

    def register(self, event, handler):
        """
        Registers an handler/callback for a specific event.

        .. attention:

            Only one handler per event is allowed. Registering a second
            handler for the same event will replace the previous registered
            handler.

        :param string event: which identifies the event. See `Slack RTM <add url>`_.
        :param function handler: is callback which will be called on the specified event.

                                .. code-block: python

                                    def event_handler_cb(rtm_message)

                                where the rtm message is a dictionary containing the original
                                rtm message which trigger the event.
        """
        self._event_handlers[event] = handler

    def connect(self):
        """
        Connects the SlackBot with the slack server.
        """
        response = self._slack_api.call("rtm.start")
        if 'url' not in response.data:
            raise SlackApiError()
        rtm_session = response.data['url']
        self._ws_client.cb = self._received_rtm_message
        self._ws_client.connect(rtm_session)

    def send(self, message, channel):
        """
        Sends a message to the specified slack channel.

        :param string message: which will be send.
        :param string channel: which uniqule identifies the channel.
        """
        response = {'id': 1, 'type': 'message', 'text': message, 'channel': channel}
        response = json.dumps(response)
        self._ws_client.send(response)

    def close(self):
        """
        Closes the connection to the slack server.
        """
        self._ws_client.close()

    def _received_rtm_message(self, message):
        rtm_message = json.loads(message.data.decode("utf-8"))
        if 'type' not in rtm_message:
            warning = 'Received untyped rtm message! Message: {0}'
            warning = warning.format(rtm_message)
            logging.warning(warning)
        else:
            event = rtm_message['type']
            self._dispatch_event(event, rtm_message)

    def _dispatch_event(self, event, rmt_message):
        """
        Calls the appropriate event handler.

        :param string event: which indicates the type of event.
        :param rmt_message: which triggered the event.
        """
        self._event_handlers[event](rmt_message)

    def _default_handler(self, rtm_message):
        """
        The default handler which deals with all events no handler is registered for.

        :param dict rtm_message: which triggered the event.
        """
        pass


class SirTalkALot(SlackBot):
    """
    A slackbot with a basic service system.
    """

    def __init__(self, authentication_token):
        """
        Creates a new SirTalkALot instance.

        :param authentication_token: which will be used to authenticate against the slack api.
        """
        super().__init__(authentication_token, websocket.BasicWebSocketHandler)
        self._authentication_token = authentication_token
        self._slack_api = SlackApi(self._authentication_token)
        self._ping_timeout_in_seconds = 10
        self._services = {}
        self._initialize_default_services()
        self.register('message', self._message_handler)

    def _initialize_default_services(self):
        """
        Initialize and add the default services slackbot will provide.
        """
        for service in self._discover_all_service_plugins():
            service_instance = service()
            service_instance.init()
            self.add_service(service_instance)
        self.add_service(services.Help(self._services))

    def _message_handler(self, rtm_message):
        """
        Handels, dispatches incoming text messages.
        :param rtm_message: which contains the text message.
        """
        if 'text' not in rtm_message:
            warning = 'Received message event without message. Message: {0}'
            warning = warning.format(rtm_message)
            logging.warning(warning)
        else:
            arguments = rtm_message['text'].strip()
            arguments = arguments.split(' ')
            service_name = arguments[0]
            arguments = arguments[1:]
            if service_name in self._services:
                service = self._services[service_name]
                response = service.handle_request(arguments)
                self.send(response, rtm_message['channel'])

    @staticmethod
    def _discover_all_service_plugins():
        services = []
        for entry_point in pkg_resources.iter_entry_points('sirtalkalot.plugin.services'):
            services.append(entry_point.load())
        return services

    def close(self):
        for service in self._services:
            service.shutdown()
        super().close()

    def add_service(self, service):
        """
        Adds a service to the SirTalkALot service system.

        :param service: which will be added.
        """
        self._services[service.name] = service

    @staticmethod
    def main():
        """
        Usage:
          sirtalkalot [--auth-token=<token>] [--deamon] [-h] [-v]

        Options:
          -h --help             Show this screen.
          -v --version          Show version.
          --deamon              deamonize sir talkalot
          --auth-token=<token>  The authentication token which will be used to access
                                the slack api.
                                As an alternative you can specify it in the .slackyrc
                                or set the $SLACK_API_TOKEN environment variable.
        """
        args = docopt.docopt(doc=SirTalkALot.main.__doc__, version='0.0.1')
        sirtalkalot = SirTalkALot(args['--auth-token'])
        sirtalkalot.connect()

def main():
    SirTalkALot.main()


if __name__ == '__main__':
    main()



