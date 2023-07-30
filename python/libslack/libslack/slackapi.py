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
import json
import urllib.parse
import http.client
from libslack.version import LIBRARY_VERSION

__author__ = 'Nicola Coretti'
__email__ = 'nico.coretti@gmail.com'
__version__ = LIBRARY_VERSION

API_BASE_URL = "https://slack.com/api/"
SLACK_DOMAIN = "www.slack.com"


class SlackApi(object):
    """
    A SlackApi object can be used to interact with the slack api.

    For futher details see `methods <https://api.slack.com/methods>`_.
    """
    SLACK_API_CALLS = {'api.test', 'auth.test', 'channels.archive',
                       'channels.create', 'channels.history', 'channels.info',
                       'channels.invite', 'channels.join', 'channels.kick',
                       'channels.leave', 'channels.list', 'channels.mark',
                       'channels.rename', 'channels.setPurpose', 'channels.setTopic',
                       'channels.unarchive', 'chat.delete', 'chat.postMessage',
                       'chat.update', 'emoji.list', 'files.info', 'files.list',
                       'files.upload', 'groups.archive', 'groups.close',
                       'groups.create', 'groups.createChild', 'groups.history',
                       'groups.invite', 'groups.kick', 'groups.leave', 'groups.list',
                       'groups.mark', 'groups.open', 'groups.rename', 'groups.setPurpose',
                       'groups.setTopic', 'groups.unarchive', 'im.close', 'im.history',
                       'im.list', 'im.mark', 'im.open', 'oauth.access', 'presence.set',
                       'rtm.start', 'search.all', 'search.files', 'search.messages',
                       'stars.list', 'users.info', 'users.list', 'users.setActive'}

    def __init__(self, authentication_token, request=None):
        """
        Creates a new Slack-Api object which can be used to interact with the slack api.

        :param string authentication_token: which grants authenticated access to the slack api.
        :param class request: which encapsulates the request logic.
        """
        self._authentication_token = authentication_token
        if not request:
            self._request = SlackApiRequest
        else:
            self._request = request

    def call(self, api_call, parameters=None):
        """
        Executes a call on the remote slack api and returns
        an appropriate :py:class:`SlackApiResponse` object.

        :param string api_call: which identifies the web api endpoint which shall be called.
        :param dict parameters: which will be supplied to the web api endpoint.

                                e.g.: ``{'channel': 'C1234567890', 'text': 'this message will be sent'}``

                                .. attention::
                                    The authentication-token allways will be passed to the endpoint implicitly.


        :return: an ApiResponse object containing the data provided
                by the slackapi endpoint.

        :raise: Exception if an unknown api method is called.
        """
        if api_call not in SlackApi.SLACK_API_CALLS:
            error_message = "Unknown api method was called"
            raise Exception(error_message)
        else:
            request = self._request(api_call, self._authentication_token)
            response = request.execute(parameters)
            return response


class SlackApiRequest(object):
    """
    The SlackApiRequest class handles and encapsulates a slack request.
    """

    def __init__(self, api_call, authentication_token):
        """
        Creates a new ApiRequest object for the specified api call.

        :param api_call: name of the api method which shall be callable by the request object.
        :param authentication_token: which will be used to authorize the api call request.
        """
        self._api_call = api_call
        self._authentication_token = authentication_token
        self._connection = http.client.HTTPSConnection(SLACK_DOMAIN)

    def execute(self, request_parameters=None):
        """
        Executes an ApiRequest, request an api call.

        :param dict request_parameters: which will be supplied to the web api endpoint.

                                e.g.: ``{'channel': 'C1234567890', 'text': 'this message will be sent'}``

                                .. attention::
                                    The authentication-token allways will be passed to the endpoint implicitly.
        :param authentication_token: which grants access to the api.

        :return: an SlackApiResponse object based on the response of the slackapi endpoint.

        :raise: Exception if an error occurs while executing the api call.
        """
        parameters = {}
        parameters.update({'token': self._authentication_token})
        if isinstance(request_parameters, dict):
            parameters.update(request_parameters)

        parameters = urllib.parse.urlencode(parameters)
        api_call_endpoint = API_BASE_URL + self._api_call
        self._connection.request("GET", api_call_endpoint + "?" + parameters)
        response = self._connection.getresponse()

        if not (response.status == http.client.OK):
            error_message = "Error while executing api call,Status: {0}, Reason: {1}"
            error_message = error_message.format(response.status, response.reason)
            raise Exception(error_message)
        else:
            response_data = response.read()
            return SlackApiResponse(response_data.decode('utf-8'))


class SlackApiResponse(object):
    """
    The SlackApiResponse class handles and encapsulates an response provided
    by the slackapi after an api method was called at the endpoint.
    """

    def __init__(self, response_data):
        """
        Interprets a response of slack api call and creates the appropriate ApiResponse object.

        :param response_data: a json string which is a valid response for
                              a slackapi call. For futher detailssee `methods <https://api.slack.com/methods>`_.
        """
        self.data = json.loads(response_data)

    def is_error(self):
        """
        Indicates whether or not the response indicates that an
        error occured while trying to execute the associated api call.

        :return: True if an error has occurred, otherwise False.
        """
        if 'ok' in self.data:
            return not self.data['ok']
        else:
            return True

    def get_error_message(self):
        """
        If is_error returns True, this method returns a more detail
        error message.

        :return: a string which provides a more detail error message.
        """
        if 'error' in self.data:
            return self.data['error']
        else:
            return 'No Error'

