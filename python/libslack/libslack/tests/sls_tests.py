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
from unittest.mock import Mock, patch
from libslack.sls import SlackShell, main


class SlsTests(unittest.TestCase):

    def setUp(self):
        self._auth_token = 'XoXo-AuthToken-XXX-YYY'
        self._shell = SlackShell(self._auth_token)
        self._users = {'members': {'id': 'U1001', 'name': 'John Doe'}}
        self._channels = {'members': {'id': 'C0001', 'name': 'General', 'num_members': 10}}

    def tearDown(self):
        pass

    @patch('sys.exit')
    def test_do_quite_command_calls_exit(self, exit_mock):
        self._shell.do_quit('args')
        self._shell.postcmd(None, None)
        self.assertTrue(exit_mock.called)

    @patch('libslack.utils.try_to_get_auth_token')
    @patch('sys.argv')
    @patch('sys.exit')
    def test_main_loop_quits_because_of_missing_auth_token(self, exit_mock, argv_mock, get_auth_token_mock):
        main()
        self.assertTrue(get_auth_token_mock.called)
        exit_mock.assert_called_with(-1)

    @patch('sys.argv')
    @patch('sys.exit')
    @patch('cmd.Cmd.cmdloop')
    def test_main_loop_quits_because_of_missing_auth_token(self, cmd_mock, exit_mock, argv_mock):
        import os
        os.environ['SLACK_API_TOKEN'] = 'xxx-yyy-zzz'
        main()
        exit_mock.assert_called_with(0)
        self.assertTrue(cmd_mock.called)

    @patch('builtins.print')
    def test_if_do_list_prints_the_help_of_the_list_command_if_no_parameters_are_supplied(self, print_mock):
        self._shell.do_list('')
        print_mock.assert_called_once_with(self._shell.do_list.__doc__)

    @patch('builtins.print')
    def test_if_do_list_prints_the_help_of_the_channels_command_if_help_parameter_is_provided(self, print_mock):
        self._shell.do_list('channels -h')
        print_mock.assert_called_once_with(self._shell._list_channels.__doc__)

    @patch('builtins.print')
    def test_if_do_list_prints_the_help_of_the_users_command_if_help_parameter_is_provided(self, print_mock):
        self._shell.do_list('users -h')
        print_mock.assert_called_once_with(self._shell._list_users.__doc__)

    @patch('libslack.slackapi.SlackApi')
    @patch('builtins.print')
    def test_if_do_list_prints_the_user_list_if_the_users_arg_is_provided(self, print_mock, slack_api_mock):
        response_mock = Mock()
        response_mock.data = self._users
        slack_api_mock.call = response_mock
        shell = SlackShell(self._auth_token)
        shell.do_list('users')
        self.assertTrue(print_mock.called)

    @patch('libslack.slackapi.SlackApi')
    @patch('builtins.print')
    def test_if_do_list_prints_the_channel_list_if_the_channels_arg_is_provided(self, print_mock, slack_api_mock):
        response_mock = Mock()
        response_mock.data = self._users
        slack_api_mock.call = response_mock
        shell = SlackShell(self._auth_token)
        shell.do_list('channels')
        self.assertTrue(print_mock.called)


if __name__ == '__main__':
    unittest.main()
