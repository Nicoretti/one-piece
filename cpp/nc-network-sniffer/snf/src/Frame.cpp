/**
 * Copyright (C) 2013, Nicola Coretti
 *
 * Author: Nicola Coretti
 * Version: 0.1.0
 * Contact: nico.coretti@googlemail.com
 */

#include "Frame.h"
#include "Exception.h"
#include <string.h>


Frame::Frame(uint8_t* buffer, uint32_t data_length, uint32_t buffer_length, uint32_t frame_id) 
: _buffer(buffer), _data_length(data_length), _buffer_length(buffer_length), _frame_id(frame_id) {}

uint32_t Frame::GetFrameId() {

    return this->_frame_id;;
}

uint8_t* Frame::GetBuffer() {

    return this->_buffer;
}

uint32_t Frame::GetBufferLength() {

    return this->_buffer_length;
}

uint32_t Frame::GetDataLength() {

    return this->_data_length;
}

uint8_t& Frame::operator[](uint32_t index) {

    if (index >= (this->_data_length)) {
        
        throw Exception("Index out of range");
    }

    return this->_buffer[index];
}

const uint8_t& Frame::operator[](uint32_t index) const {

    if (index >= (this->_data_length)) {
        
        throw Exception("Index out of range");
    }

    return this->_buffer[index];
}

Frame::~Frame() {}
