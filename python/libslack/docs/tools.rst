Tools
=====

Slack CMD (scmd)
----------------
The Slack CMD enables its user to use the slack web api via the command line.

Usage
*****

.. code-block:: console

    Usage:

    scmd (API_COMMAND | -h | -v ) [<params>] [--auth-token=<token>]

    Options:
      -h                    Show this screen.
      -v                    Show version.
      --auth-token=<token>  The authentication token which will be used to access
                            the slack api.
                            As an alternative you can specify it in the .slackrc
                            or set the $SLACK_API_TOKEN environment variable.


Example
*******

Call auth.test method
+++++++++++++++++++++
.. code-block:: console

    User@Host ~ $ scmd auth.test --auth-token xoxb-xxxxxxxxxx-yyyyyyyyyyyyyyyyyyyyyyyy
    {'user_id': 'UXXXXXXXX', 'url': 'https://teamname.slack.com/', 'team': 'Teamname', 'user': 'username', 'team_id': 'TXXXXXXXX', 'ok': True}

Send a chat message using the web api
+++++++++++++++++++++++++++++++++++++
.. code-block:: console

    User@Host ~ $ scmd chat.postMessage "{'channel': 'CXXXXXXXX', 'text': 'this is a message send fd from the command line ;)'}" --auth-token="xoxp-xxxxxxxxxx-yyyyyyyyyy-xxxxxxxxxx-yyyyyy"
    {'ok': True, 'message': {'username': 'bot', 'subtype': 'bot_message', 'ts': '1445633421.000121', 'text': 'this is a message send fd from the command line ;)', 'type': 'message'}, 'ts': '1445633421.000121', 'channel': 'CXXXXXXXX'}

Slack Shell (sls)
-----------------
The Slack Shell provides an interactive shell which enables the user to interactively interact
with the slack web api (e.g. query all registered users).

Usage
*****

.. code-block:: console

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


Screenshot
**********

.. image:: _static/sls.png

