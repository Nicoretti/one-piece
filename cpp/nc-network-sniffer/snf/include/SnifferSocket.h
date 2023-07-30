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
class SnifferSocket {

private:

    int _socket_fd;

    int _interface_index;

    std::string* _ifname;


    /**
     * Checks wether this is a a local generated packet with itself as destination.
     *
     * @param buffer: raw data of the ethernet packet.
     * @param buffer_size: size of the raw data buffer.
     *
     * @return: <code>true</code> if it is a local to local packet,
     *          otherwise <code>false</code>.
     */
    bool IsLocalToLocal(uint8_t* buffer, uint32_t buffer_size);

    /**
     * Creates a new socket which will be used for this sniffer socket.
     *
     * Initialization method.
     */
    void CreateSocket();

    /**
     * Toggles the promiscuous mode setting of the interface
     * this SinfferSocket is associated with.
     */
    void TogglePromiscuousMode();

    /**
     * Binds the socket to an interface. The Interface which will
     * be associated with this SnifferSocket.
     */
    void Bind();

public:

    /**
     * Creates a new SnifferSocket for the specified interface.
     *
     * @param ifname: name of the network interface which will 
     *                be used for sniffing.
     */
    SnifferSocket(const char* ifname);

    /**
     * Enables the promiscuous mode of the interface this SnifferSocket
     * is attached to.
     */
    void EnablePromiscuousMode();

    /**
     * Disables the promiscuous mode of the interface this 
     * SnifferSocket is attached to.
     */
    void DisablePromiscuousMode();

    /**
     * Receives a message from the socket.
     * If no message is available at the socket, this calls waits/blocks.
     *
     * @return a new message, the ownership of the message is transferd to 
     * the caller of this method, therfore the caller  is responsible for it's delition.
     */
    Message* ReceiveMessage();

    /**
     * Cleans up the mess.
     */
    ~SnifferSocket();

    /**
     * Checks whether the interface this SnifferSocket is attached
     * to is in promiscuous mode or not.
     *
     * @param ifname: interface which will be checked.
     *
     * @return <code>true</code> if the interface is in promiscuous
     *          mode, otherwise <code>false</code>.
     */
    static bool IsInterfaceInPromiscuousMode(const char* ifname);

    /**
     * Checks wether the given interface name is valid or not.
     *
     * @param ifname: interface name which will be checked.
     *
     * @return <code>true</code> if the interface name is valid,
     *         otherwise <code>false</code>.
     */
    static bool IsInterfaceNameValid(const char* ifname);

    /**
     * Gets the interface index for an interface.
     *
     * @param ifname: interface name whose interface index will be retrieved.
     *                has to be a vlaid interface name 
     *                @see SnifferSocket#IsInterfaceNameValid
     *
     * @return the interface index of the specified interface.
     */
    static int GetInterfaceIndex(const char* ifname);
}; 

#endif /* SNIFFER_SOCKET_H */
