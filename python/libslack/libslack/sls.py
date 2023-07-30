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

import cmd
import sys

import docopt

from libslack import slackapi
from libslack.utils import try_to_get_auth_token
from libslack.version import VERSION_TEMPLATE

__author__ = 'Nicola Coretti'
__email__ = 'nico.coretti@gmail.com'
__version__ = VERSION_TEMPLATE.format(major=0, minor=1, patch=0)


class SlackShell(cmd.Cmd):

    def __init__(self, auth_token):
        """
        Creates a new SlackShell which can be used to query various data from the slack server.

        :param string auth_token: which will be used authenticate against the slack server.
        """
        self.intro = "Slack Shell (SLS)\nTo get help type help\n"
        self.prompt = "((SLS)) >>> "
        super().__init__()
        self.slack_api = slackapi.SlackApi(auth_token)
        self._quit = False

    def _list_channels(self, args):
        """
        Lists all channels registered at the slack team the access token is associated with.

        Options:
            -h      prints this help.

        Output-Format:
        ID  Channel-Name   Members
        """
        channels = self.slack_api.call("channels.list").data['channels']
        fmt_string = "ID: {0} \t{1}\tNumber of Members: {2}"
        fmt_string = "| {0:^15} | {1:^30} | {2:^10} |"
        print(fmt_string.format('Channel-Id', 'Channel-Name', 'Members'))
        print('|' + '-' * 17 + '|' + '-' * 32 + '|' + '-' * 12 + "|")
        fmt_string = "| {0:<15} | {1:<30} | {2:>10} |"
        for channel in channels:
            cid = channel['id'] if 'id' in channel else None
            name = channel['name'] if 'name' in channel else None
            number_of_members = channel['num_members'] if 'num_members' in channel else None
            print(fmt_string.format(cid, name, number_of_members))

    def _list_users(self, args):
        """
        Lists all users registered at the slack team the access token is associated with.

        Options:
            -h      prints this help.

        Output-Format:
        ID  User-Name
        """
        members = self.slack_api.call("users.list").data['members']
        member_dict = {}
        fmt_string = "| {0:^15} | {1:^30} |"
        print(fmt_string.format('User-Id', 'User-Name'))
        print('|' + '-' * 50 + '|')
        fmt_string = "| {0:<15} | {1:<30} |"
        for member in members:
            uid = member['id'] if 'id' in member else None
            name = member['name'] if 'name' in member else None
            print(fmt_string.format(uid, name))

    def do_list(self, args):
        """
        The list command can be used to query various information fon the slack server.

        Usage:
            list channels [-h]
            list users [-h]

        Options:

            -h  prints help for the preceding command.
        """
        args.strip()
        arguments = args.split()
        if not arguments:
            print(self.do_list.__doc__)
        else:
            if 'channels' in arguments:
                if '-h' in arguments:
                    print(self._list_channels.__doc__)
                else:
                    self._list_channels(arguments)
            elif 'users' in arguments:
                if '-h' in arguments:
                    print(self._list_users.__doc__)
                else:
                    self._list_users(arguments)

    def do_quit(self, args):
        """
        Quits the SlackShell.
        :params: all specified parameters will be dropped.
        """
        self._quit = True

    def postcmd(self, stop, args):
        if self._quit:
            sys.exit(0)

def main():
    """
    Usage:
      sls [--auth-token=<token>]
      sls -h | --help
      sls -v | --version

    Options:
      -h --help             Show this screen.
      -v --version          Show version.
      --auth-token=<token>  The authentication token which will be used to access
                            the slack api.
                            As an alternative you can specify it in the .slackyrc
                            or set the $SLACK_API_TOKEN environment variable.
    """
    args = docopt.docopt(doc=main.__doc__, version='0.0.1')
    auth_token = try_to_get_auth_token(args)
    if not auth_token:
        print("Error: No authentication token available!", file=sys.stderr)
        sys.exit(-1)
    else:
        SlackShell(auth_token).cmdloop()
        sys.exit(0)


if __name__ == "__main__":
    main()
