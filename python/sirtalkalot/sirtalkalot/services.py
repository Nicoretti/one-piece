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
import random

__version__ = "0.0.1"
__author__ = 'Nicola Coretti'
__email_ = 'nico.coretti@gmail.com'


class AbstractService(object):
    """
    Implements the basic service interface necessary to be used as bot service. """

    def __init__(self, name, usage, help):
        """
        An abstract service implements the basic properties a service have to provide.

        :param name: name of the service.
        :param usage: a brief description how to call the service.
        :param help: a detailed help about parameters and options which can
                     be supplied with requests.
        :return:

        .. attention:

            A class which wanna make use of this basic implementation has to
            inherit from the service class and overwrite the `handle_request`
            method.
        """
        self._name = name
        self._usage = usage
        self._help = help

    @property
    def name(self):
        return self._name

    @property
    def usage(self):
        return self._usage

    @property
    def help(self):
        return self._help

    def init(self):
        pass

    def run(self):
        pass

    def shutdown(self):
        pass

    def handle_request(self, arguments):
        """
        Does the actual work the service provides.

        :param list arguments: which where supplied along with the request.

        :return: a string containing response of the service.
        :rtype: string
        """
        raise NotImplementedError()


class Help(AbstractService):

    def __init__(self, services):
        help = """
        Help for SirTalkalot.

        Usage:
            help                    prints this help.
            help -services    lists all available services.
            help <servicename>      print the help of the specified service.
        """
        usage ="""
        Usage:
            help                    prints this help.
            help -services    lists all available services.
            help <servicename>      print the help of the specified service.
        """
        self._services = services
        super().__init__('help', usage, help)

    def handle_request(self, arguments):
        """
        Provides help for multiple services.

        :param arguments: see usage.

        :return: help string.
        :rtype: string
        """
        help = """
        Services:

        {0}

        For detailed information about a service type:

            help <servicename>

        """
        if '-services' in arguments:
            services = ''
            for service in self._services:
                services += '* {0}\n'.format(service)
            return help.format(services)
        elif len(arguments) > 0 and arguments[0] in self._services:
            return self._services[arguments[0]].help
        else:
            return self.help


class ZenOfPython(AbstractService):

    ZEN = """
    The Zen of Python, by Tim Peters

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
    """

    def __init__(self):
        help = """
        The Zen service provides the zen of python if its called.

        Usage:
            zen
        """
        usage ="""
        Usage:
            zen
        """
        super().__init__('zen', usage, help)

    def handle_request(self, arguments):
        """
        Provides the ZEN of python.

        :param arguments: will be ignored.

        :return: the ZEN of python.
        :rtype: string
        """
        return self.ZEN


class ChuckNorris(AbstractService):

    JOKES = [
        "When Alexander Bell invented the telephone he had 3 missed calls from Chuck Norris",
        "The flu gets Chuck Norris shots",
        "Fear of spiders is aracnaphobia, fear of tight spaces is chlaustraphobia, fear of Chuck Norris is called Logic",
        "There used to be a street named after Chuck Norris, but it was changed because nobody crosses Chuck Norris and lives.",
        "Chuck Norris died 20 years ago, Death just hasn't built up the courage to tell him yet.",
        "If you rate this 5 roundhouse kicks, then Chuck Norris WILL roundhouse kick Justin Bieber's ass.",
        "Chuck Norris has already been to Mars; that's why there are no signs of life.",
        "Some magicans can walk on water, Chuck Norris can swim through land.",
        "Chuck Norris and Superman once fought each other on a bet. The loser had to start wearing his underwear on the outside of his pants.",
        "Chuck Norris has a grizzly bear carpet in his room. The bear isn't dead it is just afriad to move.",
        "Chuck Norris once urinated in a semi truck's gas tank as a joke....that truck is now known as Optimus Prime.",
        "Chuck Norris doesn't flush the toilet, he scares the sh*t out of it",
        "Chuck Norris doesn't call the wrong number. You answer the wrong phone.",
        "Chuck Norris can cut through a hot knife with butter",
        "Chuck Norris counted to infinity - twice.",
        "Chuck Norris is the reason why Waldo is hiding.",
        "Death once had a near-Chuck Norris experience",
        "Chuck Norris can slam a revolving door.",
        "When the Boogeyman goes to sleep every night, he checks his closet for Chuck Norris.",
        "Chuck Norris once kicked a horse in the chin. Its decendants are known today as Giraffes.",
        "Chuck Norris will never have a heart attack. His heart isn't nearly foolish enough to attack him.",
        "Chuck Norris once got bit by a rattle snake........ After three days of pain and agony ..................the rattle snake died",
        "Chuck Norris can win a game of Connect Four in only three moves.",
        "Chuck Norris doesn't want to be cool, cool wants to be Chuck Norris",
        "Chuck Norris can light a fire by rubbing two ice-cubes together.",
        "When Chuck Norris does a pushup, he isn't lifting himself up, he's pushing the Earth down.",
        "There is no theory of evolution. Just a list of animals Chuck Norris allows to live.",
        "Chuck Norris doesn’t wear a watch. HE decides what time it is.",
        "The original title for Alien vs. Predator was Alien and Predator vs Chuck Norris.",
        "The film was cancelled shortly after going into preproduction. No one would pay nine dollars to see a movie fourteen seconds long.",
        "Chuck Norris doesn't read books. He stares them down until he gets the information he wants.",
        "Whenever people are holding wooden boards, Chuck Norris breaks them in half. Then he breaks the boards.",
        "Chuck Norris has no shadow....nothing's stupid enough to follow Chuck Norris.",
        "The best part of waking up is not the Folgers in your cup, it's knowing that Chuck Norris didn't kill you in your sleep.",
        "Outer space exists because it's afraid to be on the same planet with Chuck Norris.",
        "When Chuck Norris takes a test, the test answers HIS questions.",
        "If you spell Chuck Norris in Scrabble, you win. Forever.",
        "Chuck Norris made a Happy Meal cry.",
        "Chuck Norris destroyed the periodic table, because Chuck Norris only recognizes the element of surprise.",
        "Chuck Norris can play Techno music on a harmonica",
        "Chuck Norris' hand is the only hand that can beat a Royal Flush.",
        "Some people wear Superman pajamas. Superman wears Chuck Norris pajamas.",
        "Chuck Norris does not sleep. He waits.",
        "They once made a Chuck Norris toilet paper, but there was a problem: It wouldn't take shit from anybody.",
        "Some people can ride their bikes with no handle bars. but chuck norris can ride his handlebars with no bike.",
        "Chuck Norris never loses at dodgeball because the ball wants to dodge Chuck Norris.",
        "Chuck Norris doesn't breathe... He holds air hostage.",
        "Chuck Norris can drown a fish",
        "Whenever Chuck Norris came home late as a teen, his parents were grounded",
        "Chuck Norris is the only one who can kick you in the back of the face.",
        "There is no theory of evolution. Just a list of creatures Chuck Norris has allowed to live."
    ]

    def __init__(self):
        help = """
        The ChuckNorris service serves chuck norris jokes.

        Usage:
            chuck
        """
        usage = """
        Usage:
            chuck
        """
        super().__init__('chuck', usage, help)

    def handle_request(self, arguments):
        """
        Provides a random chuck norris joke.

        :param arguments: will be ignored.

        :return: a random chuck norris joke.
        :rtype: string
        """
        random_index = random.randint(0, len(self.JOKES) -1)
        return self.JOKES[random_index]


