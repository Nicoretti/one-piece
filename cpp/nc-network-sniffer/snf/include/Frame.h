/**
 * Copyright (C) 2013, Nicola Coretti
 *
 * Author: Nicola Coretti
 * Version: 0.1.0
 * Contact: nico.coretti@googlemail.com
 */

#ifndef FRAME_H
#define FRAME_H

#include <stdint.h>

/**
 * A Frame is a wrapper around a buffer. It has a data length a buffer length
 * an id and the buffer itself.
 */
class Frame {

private:
    
    uint8_t* _buffer;

    uint32_t _data_length;

    uint32_t _buffer_length;;

    uint32_t _frame_id;

public: 

    /**
     * Creates a new Frame based on the supplied buffer and it's data.
     *
     * \param data_buffer: which will be managed by this frame.
     * \param data_length: length of the data contained in the buffer.
     * \param buffer_length: length of the specified buffer.
     *
     * \pre 
     * \post
     * \throws
     */
    explicit Frame(uint8_t* buffer, uint32_t data_length, uint32_t buffer_length, uint32_t frame_id);

    /**
     * Returns #_buffer.
     */
    uint8_t* GetBuffer();

    /**
     * Returns the length of #_buffer.
     */
    uint32_t GetBufferLength();

    /**
     * Returns the length of the data contained in #_buffer.
     */
    uint32_t GetDataLength();

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
     * Gets a byte from the payload. The paylaod index
     * starts at 0 and ends with payloadlength -1.
     *  
     * @param index: of the byte to be retrieved.
     *
     * @return reference to the payload byte.
     */
    const uint8_t& operator[](uint32_t index) const;

    /**
     * Gets the id of this Frame.
     */
    uint32_t GetFrameId();
    
    /**
     * Cleans up the mess.
     */
    virtual ~Frame(); 
};

#endif /* FRAME_H */
