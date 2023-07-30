/**
 * Copyright (C) 2012, Nicola Coretti
 *
 * Author: Nicola Coretti
 * Version: 0.1.0
 * Contact: nico.coretti@googlemail.com
 */

#include <string>
#include "Exception.h"

Exception::Exception() {

    this->_message = new std::string("");
    this->_cause = NULL;
}

Exception::Exception(const char* message) {

    this->_message = new std::string(message);
    this->_cause = NULL;
}

Exception::Exception(const char* message, Exception* cause) {

    this->_message = new std::string(message);
    this->_cause = cause;
}

Exception::Exception(Exception* cause) {

    this->_message = new std::string("");
    this->_cause = cause;
}

const char* Exception::GetMessageAsCString() {

    return this->_message->c_str();
}

std::string* Exception::GetMessage() {

    return this->_message;
}

Exception::~Exception() {

    if (this->_cause != NULL) { delete this->_cause; }
    if (this->_message != NULL) { delete this->_message; }
}
