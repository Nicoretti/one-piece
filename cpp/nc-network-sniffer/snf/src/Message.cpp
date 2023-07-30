/**
 * Copyright (C) 2012, Nicola Coretti
 *
 * Author: Nicola Coretti
 * Version: 0.1.0
 * Contact: nico.coretti@googlemail.com
 */

#include "Message.h"
#include "Exception.h"
#include <string.h>

uint32_t Message::_id_counter = 1;

const char* Message::GetLayer4Protocol() {

    const char* l4_protocol = NULL;
    uint8_t l4_type_field;
    // select field which indicates the next higher protocol type
    // 0x0800 = IPv4
    if ( this->_type == 0x0800) {

       l4_type_field  = this->_data_buffer[23];
    }
    // 0x86DD = IPv6
    else if (this->_type == 0x86DD) {

        l4_type_field = this->_data_buffer[20];
    }

    // determine protocol
    switch (l4_type_field) {

        case 0x01:
            l4_protocol = "ICMP";
            break;

        case 0x06:
            l4_protocol = "TCP";
            break;

        case 0x11:
            l4_protocol = "UDP";
            break;

        case 0x3a:
            l4_protocol = "ICMPv6";
            break;

        default:
            l4_protocol = "---";
            break;
    }

    return l4_protocol;
}

Message::Message(uint8_t* data_buffer, uint32_t buffer_length, uint32_t data_length) {

    this->_data_buffer = data_buffer;
    this->_data_buffer_length = buffer_length;
    this->_data_length = data_length;
    this->_payload = data_buffer + 14;
    this->_payload_length = this->_data_length - 14;
    this->_type = ((uint16_t) (data_buffer[12] << 8)) | ((uint16_t) data_buffer[13]);
    this->_message_id = Message::_id_counter++;
    this->_src_address = new uint8_t[6];
    this->_dst_address = new uint8_t[6];
    (void) memcpy(this->_dst_address, data_buffer, 6);
    (void) memcpy(this->_src_address, data_buffer + 6, 6);
}

uint32_t Message::GetMessageId() {

    return this->_message_id;
}

uint8_t* Message::GetDataBuffer() {

    return this->_data_buffer;
}

uint32_t Message::GetDataBufferLength() {

    return this->_data_buffer_length;
}

uint32_t Message::GetDataLength() {

    return this->_data_length;
}

uint8_t* Message::GetPayload() {

    return this->_payload;
}

uint32_t Message::GetPayloadLength() {

    return this->_payload_length;
}

uint8_t* Message::GetSourceAddress() {

    return this->_src_address;
}

uint8_t* Message::GetDestinationAddress() {

    return this->_dst_address;
}

uint8_t& Message::operator[](uint32_t index) {

    if (index >= (this->_payload_length)) {
        
        throw Exception("Index out of range");
    }

    return this->_payload[index];
}

uint16_t Message::GetType() {

    return this->_type;
}

Message::~Message() {

    if (this->_data_buffer != NULL) { delete this->_data_buffer; }
    if (this->_src_address != NULL) { delete this->_src_address; }
    if (this->_dst_address != NULL) { delete this->_dst_address; }
}
