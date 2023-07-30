/**
 * Copyright (C) 2012, Nicola Coretti
 *
 * Author: Nicola Coretti
 * Version: 0.1.0
 * Contact: nico.coretti@googlemail.com
 */

#ifndef PRETTY_PRINTER_H
#define PRETTY_PRINTER_H

#include "Message.h"
#include <stdint.h>

/**
 * A PrettyPrinter is used to print various strings to the stdout. 
 */
class PrettyPrinter {

private:

    /**
     * Gets a printeable ascii char for a given byte.
     */
    char GetCharForByte(uint8_t byte);

    /**
     * Gets the protocolname of the given type id.
     */
    const char* GetProtocolName(uint16_t  type);
    
    /**
     * Pretty prints up to 16 bytes of the payload to the stdout.
     */
    void PrintPayloadLine(uint8_t* bytes, uint16_t byte_count);

    /**
     * Pretty prints the whole payload of the message to the stdout.
     */
    void PrintPayload(Message* message);

    /**
     * Pretty print the header of the message.
     */
    void PrintMessageHeader(Message* message);


public:

    /**
     * Creates a new PrettyPrinter.
     */
    PrettyPrinter();

    /**
     * Prints a message on the stdout.
     */
    void PrintMessage(Message* message);

};

#endif /* PRETTY_PRINTER_H */
