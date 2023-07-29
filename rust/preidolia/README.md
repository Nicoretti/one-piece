# What This Project is For
Actually I am personally a big fan of the [Synalyze It](https://www.synalysis.net)/[Hexinator](https://hexinator.com) tool. It's great when for analyzing blob or while you create
new binary format. It provides a quick and very reliable way to parse the formats for either finding issue within
the blob on quickly modifing it etc., while the tool and its parsing engine is Amazing it has one major issue:

    1. You only can access its functionality via GUI! 
    (Yes there are scripts to export the parsed data etc. to xml but also in order to execute those scripts you need to run them via the GUI first)
    
The main Idea of this Project is to also understand the grammar definitions of [Synalyze It](https://www.synalysis.net)/[Hexinator](https://hexinator.com) and create parsers from 
it, but instead making the results and functionality available via gui, this Project strives to provide a command line output(s) 
which then in turn can be used for further processing.

# Goals
* Understand [Synalyze It](https://www.synalysis.net)/[Hexinator](https://hexinator.com) - grammar files
* Define output format(s) for a "generic" decoding command line tool
* Define input format(s) for a "generic" encoding command line tool

# Non Goals
* Replace [Synalyze It](https://www.synalysis.net)/[Hexinator](https://hexinator.com)
* Implement a GUI for grammar editing or parser and results

# Unleash the power of encoding/decoding
TBD - exmaples mini servers etc. based cli combination of e.g. socat and encoder/decoder

