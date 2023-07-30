/**
 * Copyright (C) 2012, Nicola Coretti
 *
 * Author: Nicola Coretti
 * Version: 0.1.0
 * Contact: nico.coretti@googlemail.com
 */

#ifndef SNIFFER_SOCKET_H
#define SNIFFER_SOCKET_H

#include "Message.h"

// socket includes
#include <sys/types.h>
#include <sys/socket.h>

// netdevice includes
#include <sys/ioctl.h>
#include <net/if.h>

// perror includes
#include <stdio.h>
#include <errno.h>

#include <string>

/**
 * A Sniffer socket can be used to network traffic on a
 * network interface. 
 */
class ISnifferSocket {

public:

    /**
     * Enables the promiscuous mode of the interface this SnifferSocket
     * is attached to.
     */
    virtual void EnablePromiscuousMode() = 0;

    /**
     * Disables the promiscuous mode of the interface this 
     * SnifferSocket is attached to.
     */
    virtual void DisablePromiscuousMode() = 0;

    /**
     * Receives a message from the socket.
     * If no message is available at the socket, this calls waits/blocks.
     *
     * @return a new message, the ownership of the message is transferd to 
     * the caller of this method, therfore the caller  is responsible for it's delition.
     */
    virtual Frame* GetNextFrame() = 0;

    /**
     * Cleans up the mess.
     */
    virtual ~ISnifferSocket() = 0;

    /**
     * Checks whether the interface this SnifferSocket is attached
     * to is in promiscuous mode or not.
     *
     * @param ifname: interface which will be checked.
     *
     * @return <code>true</code> if the interface is in promiscuous
     *          mode, otherwise <code>false</code>.
     */
     virtual bool IsInterfaceInPromiscuousMode(const char* ifname) = 0;

    /**
     * Gets the interface index for an interface.
     *
     * @param ifname: interface name whose interface index will be retrieved.
     *                has to be a vlaid interface name 
     *                @see SnifferSocket#IsInterfaceNameValid
     *
     * @return the interface index of the specified interface.
     */
     virtual int GetInterfaceIndex(const char* ifname) = 0;
}; 

#endif /* ISNIFFER_SOCKET_H */
