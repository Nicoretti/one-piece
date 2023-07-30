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
import os
import sys
from libslack.slackapi import SlackApi
from libslack.scmd import main
from docopt import DocoptExit

class ScmdTest(unittest.TestCase):

    def setUp(self):
        pass

    @patch('sys.argv')
    @patch('sys.exit')
    def test_main_usage_is_printed_if_invalid_parameres_are_specified(self, exit_mock, argv_mock):
        self.assertRaises(DocoptExit, main)

    @patch.object(sys, 'argv', ['scmd.py', 'api.test'])
    def test_main_exits_with_due_to_missing_auth_token(self):
        self.assertRaises(SystemExit, main)

    @patch('libslack.slackapi.SlackApi', spec=SlackApi)
    @patch.object(sys, 'argv', ['scmd.py', 'api.test'])
    @patch.object(os, 'environ', {'SLACK_API_TOKEN': 'xxx-yyy-zzz'})
    def test_main_exits_if_an_error_response_is_returned(self, slackapi_mock):
        slackapi_mock.return_value.call.return_value.response.return_value.is_error.return_value = True
        self.assertRaises(SystemExit, main)

if __name__ == '__main__':
    unittest.main()
