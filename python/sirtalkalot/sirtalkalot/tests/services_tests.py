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
from sirtalkalot import services


class AbstractServiceTests(unittest.TestCase):

    def test_abstract_service_raises_exception_if_handle_request_is_called(self):
        abstract_service = services.AbstractService('service_name', 'usage', 'some help')
        self.assertRaises(NotImplementedError, abstract_service.handle_request, ['arg1', 'arg2'])


class ZenOfPythonTests(unittest.TestCase):

    def test_returns_the_zen_of_python(self):
        zen_service = services.ZenOfPython()
        self.assertEqual(zen_service.handle_request([]), zen_service.ZEN)


class ChuckNorrisTests(unittest.TestCase):

    def test_returns_a_random_chuck_norris_joke(self):
        chuck = services.ChuckNorris()
        joke = chuck.handle_request([])
        self.assertIn(joke, chuck.JOKES)

if __name__ == '__main__':
    unittest.main()
