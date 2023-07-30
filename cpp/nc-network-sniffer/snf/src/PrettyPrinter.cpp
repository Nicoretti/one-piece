/**
 * Copyright (C) 2012, Nicola Coretti
 *
 * Author: Nicola Coretti
 * Version: 0.1.0
 * Contact: nico.coretti@googlemail.com
 */

#include "PrettyPrinter.h"
#include <iostream>
#include <iomanip>
using namespace std;

PrettyPrinter::PrettyPrinter() {}


char PrettyPrinter::GetCharForByte(uint8_t byte) {

    char character = '.';
    if ((byte > ((uint8_t) 0x1F)) && (byte < ((uint8_t) 0x7F))) {
        
        character = (char) byte;
    }
    else {

        character = '.';
    }

    return character;
}


const char*  PrettyPrinter::GetProtocolName(uint16_t type) {

    const char* protocol = NULL;
    switch (type) {

        case 0x0800:
            protocol = "IPv4";
            break;

        case 0x86DD:
            protocol = "IPv6";
            break;

        default:
            protocol = "---";
            break;
    }

    return protocol;
}


void PrettyPrinter::PrintMessageHeader(Message* message) {

     const char* l3_protocol = this->GetProtocolName(message->GetType());

    // print header
    cout << "   #: " << setw(14) << setfill('0') << dec << message->GetMessageId();
    cout << "  Type: " << setw(4) << hex << message->GetType();
    cout << "h (" << l3_protocol << "/" << message->GetLayer4Protocol() <<")";
    cout << "  Bytes: " << dec <<  message->GetDataLength() << endl;
    cout << setw(68) << setfill('-') << "-" << endl;

    // print addresses
    cout << "SRC: " << setfill('0');
    for (int i = 0; i < 6; i++) { 
        cout << hex << setw(2) << (int) message->GetSourceAddress()[i] << " ";
    }
    cout << "  DST: ";
    for (int i = 0; i < 6; i++) { 
        cout << hex << setw(2) << (int) message->GetDestinationAddress()[i] << " ";
    }
    cout << endl << setw(68) << setfill('-') << "-" << endl;
}


void PrettyPrinter::PrintPayloadLine(uint8_t* bytes, uint16_t byte_count) {

    for (uint16_t i = 0; i < byte_count; i++) {

        cout << hex << setfill('0') << setw(2) << (int) bytes[i] << " ";
    }
    if (byte_count < 16) {
   
		uint32_t space = (16 - byte_count);
		for (uint16_t i = 0; i < space; i++) {

        	cout << "  " << " ";
		}
    }
    cout << setw(4) << setfill(' ') << " ";
    for (size_t i = 0; i < byte_count; i++) {

        cout << this->GetCharForByte(bytes[i]);
    }
    cout << endl; 
}

void PrettyPrinter::PrintPayload(Message* message) {

    for (unsigned int i = 0; i < message->GetPayloadLength() ; i++) {

        uint32_t offset = ((i / 16) - 1) * 16;
        bool is_full_line = ((i % 16) == 0) && (i != 0);
        bool is_last_line = (i == (message->GetPayloadLength() - 1));
        if (is_full_line && !is_last_line) {
            uint32_t offset = ((i / 16) - 1) * 16;
            this->PrintPayloadLine(message->GetPayload() + offset ,16);
        }
        else if (is_last_line) {
            uint16_t byte_count = message->GetPayloadLength() % 16;
            this->PrintPayloadLine(message->GetPayload() + offset, byte_count);
        }
    }
}


void PrettyPrinter::PrintMessage(Message* message) {

    this->PrintMessageHeader(message);
    this->PrintPayload(message);
    cout << endl;
}

