/**
 * Copyright (C) 2012, Nicola Coretti
 *
 * Author: Nicola Coretti
 * Version: 0.1.0
 * Contact: nico.coretti@googlemail.com
 */

#ifndef MESSAGE_H
#define MESSAGE_H

#include <stdint.h>

// TODO: Comment
/**
 * This class provides an abstraction for a raw message recieved from an
 * raw socket. It provides detailed information about:
 *  -
 *  - 
 *  - 
 *  and also makes the payload of the package available.
 */
class Message {

public:

    enum PROTOCOL { ICMP, ICMPv6, TCP, UDP,  UNKNOWN };

private:


    static uint32_t _id_counter;

    uint32_t _message_id;
    
    uint8_t* _data_buffer;

    uint32_t _data_buffer_length;

    uint32_t _data_length;

    uint8_t* _payload;

    uint32_t _payload_length;

    uint8_t* _src_address;

    uint8_t* _dst_address;
    
    uint16_t _type;

public: 

    /**
     * Creates a new Message based on the supplied buffer and it's data.
     *
     * @param raw_data_buffer: which contains the whole message data.
     * ATTENTION: The Message will take ownership of the buffer,
     *            therefore it will delete the buffer when the Message
     *            is deleted.
     * @param buffer_length: length of the supplied buffer.
     * @param data_length: amount of data in the buffer.
     *                     (buffer_length - data_length = free space in buffer)
     */
    Message(uint8_t* raw_data_buffer, uint32_t buffer_length, uint32_t data_length);

    /**
     * Returns the buffer which contains the raw data.
     */
    uint8_t* GetDataBuffer();

    /**
     * Returns the length of the raw data buffer.
     */
    uint32_t GetDataBufferLength();

    /**
     * Returns the length of the data in the buffer.
     */
    uint32_t GetDataLength();

    /**
     * Returns the buffer which contains the payload.
     */
    uint8_t* GetPayload();

    /**
     * Returns the length of the payload.
     */
    uint32_t GetPayloadLength();

    /**
     * Gets the source address. layer 2 address.
     */
    uint8_t* GetSourceAddress();

    /**
     * Gets the destination address. layer 2 address.
     */
    uint8_t* GetDestinationAddress(); 

    /**
     * Gets a byte from the payload. The paylaod index
     * starts at 0 and ends with payloadlength -1.
     *  
     * @param index: of the byte to be retrieved.
     *
     * @return reference to the payload byte.
     */
    uint8_t& operator[](uint32_t index);

    /**
     * Gets the included layer 4 protocol of this message.
     */
    const char* GetLayer4Protocol();

    /**
     * Gets the protocol type contained in this 
     * ethernet frame.
     */
    uint16_t GetType();

    /**
     * Gets the id of this message.
     */
    uint32_t GetMessageId();
    
    /**
     * Cleans up the mess.
     */
    ~Message(); 

};

#endif /* MESSAGE_H */
