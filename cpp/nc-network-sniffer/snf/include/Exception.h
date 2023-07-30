/**
 * Copyright (C) 2012, Nicola Coretti
 *
 * Author: Nicola Coretti
 * Version: 0.1.0
 * Contact: nico.coretti@googlemail.com
 */

#ifndef EXCEPTION_H
#define EXCEPTION_H

#include <string>
/**
 * Base class for all exceptions.
 */
class Exception {

protected:

    /**
     * If NULL/0 it indicates that the cause is unknown or nonexistent.
     */
    Exception* _cause;

    /**
     * Detailed message (what happend, why the exception was thrown, etc.)
     */
    std::string* _message;

public:

    /**
     * Creates a new exception.
     */
    Exception();

    /**
     * Creates a new exception with the specified message.
     * @param message: @see Exception#_message
     */
    Exception(const char* message);

    /**
     * Creates a new exception with the specified message and cause.
     * @param message: @see Exception#_message
     * @param cause:   @see Exception#_cause
     */
    Exception(const char* message, Exception* cause);

    /**
     * Creates a new exception with the specified cause.
     * @param cause:   @see Exception#_cause
     */
    Exception(Exception* cause);

    /**
     * Returns Exception#_message as c string
     */
    const char* GetMessageAsCString();

    /**
     * Returns Exception#_message.
     */
    std::string* GetMessage();

    /**
     * Cleans up the mess.
     */
    virtual ~Exception();

}; 
#endif /* EXCEPTION_H */
