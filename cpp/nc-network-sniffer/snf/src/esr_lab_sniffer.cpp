/**
 * Copyright (C) 2012, Nicola Coretti
 *
 * Author: Nicola Coretti
 * Version: 0.1.0
 * Contact: nico.coretti@googlemail.com
 *
 * Time used:
 * 1) create socket, get interface index, set interface to promisc mode
 * about 1 - 1,5h => resources (just manual pages) 
 */
#include "Exception.h"
#include "SnifferSocket.h"
#include "PrettyPrinter.h"
// determine user id
#include <unistd.h>
// exit imports
#include <stdlib.h>

#include <iostream>
#include <string.h>
using namespace std;

void PrintUsage();
            
int main(int argc, char* argv[], char* envp[]) {

    try {
        // check if the user has root prevs
        if (getuid() != 0) {
            cerr << "you have to be root in order to run this program." << endl;
            exit(EXIT_FAILURE);
        }
        // check if interface is supplied as argument
        if (argc == 2) {
            
            SnifferSocket* sniffer_sock = new SnifferSocket(argv[1]);
            PrettyPrinter* printer = new PrettyPrinter();
            while (true) {
                Message* msg = sniffer_sock->ReceiveMessage();
                printer->PrintMessage(msg);
                delete msg;
            }
        }
        // no interface supplied on cmd
        else {

            cerr << "No network interface specified!" << endl;
            PrintUsage();
            exit(EXIT_FAILURE);
        }
    }
    catch (Exception& ex) {

        cerr << ex.GetMessageAsCString() << endl;
    }
    exit(EXIT_SUCCESS);
}

void PrintUsage() {

    cout << "Usage: sniffer INTERFACE" << endl;
    cout << "A simple network sniffer" << endl;
    cout << endl << "version 0.1.0, Nicola Coretti" << endl;
}
