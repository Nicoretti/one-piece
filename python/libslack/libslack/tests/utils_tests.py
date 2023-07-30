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
import io
import os
import unittest

from libslack.utils import try_get_auth_token_from_environment, try_get_auth_token_from_rc_file, try_to_get_auth_token

class TryGetAuthTokenRcFileTests(unittest.TestCase):

    def setUp(self):
        self.rc_file = """
        [auth]
        API-TOKEN=XoXa-MyAuthTOken123LooksLikeThis1

        """
        self.rc_file = io.StringIO(self.rc_file)

        self.invalid_rc_file = """
        API-TOKEN=XoXa-MyAuthTOken123LooksLikeThis1

        """
        self.invalid_rc_file = io.StringIO(self.invalid_rc_file)

        self.rcfile_without_auth_token = """
        [auth]
        username=Slackuser

        """
        self.rcfile_without_auth_token = io.StringIO(self.rcfile_without_auth_token)

    def tearDown(self):
        pass

    def test_returns_none_because_of_invalid_rc_file(self):
        auth_token = try_get_auth_token_from_rc_file(self.invalid_rc_file)
        self.assertEqual(None, auth_token)

    def test_returns_none_because_no_auth_token_was_found_in_rc_file(self):
        auth_token = try_get_auth_token_from_rc_file(self.rcfile_without_auth_token)
        self.assertEqual(None, auth_token)

    def test_returns_token_found_in_rcfile(self):
        auth_token = try_get_auth_token_from_rc_file(self.rc_file)
        self.assertEqual("XoXa-MyAuthTOken123LooksLikeThis1", auth_token)


class TryGetAuthTokenFromEnvironmentTests(unittest.TestCase):

    def setUp(self):
        if 'SLACK_API_TOKEN' in os.environ:
            del os.environ['SLACK_API_TOKEN']

    def tearDown(self):
        pass

    def test_returns_none_because_the_contents_of_the_environement_var_is_empty(self):
        os.environ['SLACK_API_TOKEN'] = ''
        self.assertEqual(None, try_get_auth_token_from_environment())

    def test_returns_none_because_no_auth_token_was_found_in_environment(self):
        self.assertEqual(None, try_get_auth_token_from_environment())

    def test_returns_token_found_in_environment(self):
        auth_token = "XoXa-MyAuthTOken123LooksLikeThis1"
        os.environ['SLACK_API_TOKEN'] = auth_token
        self.assertEqual(auth_token, try_get_auth_token_from_environment())

class TryGetAuthTokenTests(unittest.TestCase):

    def setUp(self):
        if 'SLACK_API_TOKEN' in os.environ:
            del os.environ['SLACK_API_TOKEN']
        self.rc_file = os.path.join(os.environ['HOME'], '.slackrc')


    def tearDown(self):
        pass

    def test_returns_token_found_in_args(self):
        auth_token = "XoXa-MyAuthTOken123LooksLikeThis1"
        args = {'--auth-token': auth_token}
        self.assertEqual(auth_token, try_to_get_auth_token(args))

    def test_returns_none_because_the_contents_of_the_environement_var_is_empty(self):
        os.environ['SLACK_API_TOKEN'] = ''
        self.assertEqual(None, try_to_get_auth_token({}))

    def test_returns_none_because_no_auth_token_was_found_in_environment(self):
        self.assertEqual(None, try_to_get_auth_token({}))

    def test_returns_token_found_in_environment(self):
        auth_token = "XoXa-MyAuthTOken123LooksLikeThis1"
        os.environ['SLACK_API_TOKEN'] = auth_token
        self.assertEqual(auth_token, try_to_get_auth_token({}))

if __name__ == '__main__':
    unittest.main()
