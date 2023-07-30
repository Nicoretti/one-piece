/**
 * Copyright (C) 2012, Nicola Coretti
 *
 * Author: Nicola Coretti
 * Version: 0.1.0
 * Contact: nico.coretti@googlemail.com
 */
#include "Exception.h"
#include "SnifferSocket.h"

#include <arpa/inet.h>
#include <netpacket/packet.h>
#include <net/ethernet.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>
using namespace std;

void SnifferSocket::CreateSocket() {

    this->_socket_fd = socket(AF_PACKET, SOCK_RAW, 0);
    if (this->_socket_fd == -1) {
        throw Exception(strerror(errno));
    }
}

void SnifferSocket::TogglePromiscuousMode() {

    ifreq request;
    strncpy(request.ifr_name, this->_ifname->c_str(), IFNAMSIZ);
    request.ifr_flags ^= IFF_PROMISC;
    if (ioctl(this->_socket_fd, SIOCSIFFLAGS, &request) == -1) {
        throw Exception(strerror(errno));
    }
}

void SnifferSocket::Bind() {

    sockaddr_ll addr;
    addr.sll_family = AF_PACKET;
    addr.sll_protocol = htons(ETH_P_ALL);
    addr.sll_ifindex = this->_interface_index;
    //addr.sll_pkttype = PACKET_OTHERHOST;
    
    if ((bind(this->_socket_fd, (sockaddr*) &addr, sizeof(addr))) == -1) {
        throw Exception(strerror(errno));
    }
}

SnifferSocket::SnifferSocket(const char* ifname) {

    if (SnifferSocket::IsInterfaceNameValid(ifname)) { 
        this->_ifname = new string(ifname);
    } 
    else {
        throw Exception("Invalid interface name.");
    }
    this->_interface_index = SnifferSocket::GetInterfaceIndex(ifname);
    this->CreateSocket();
    this->EnablePromiscuousMode();
    this->Bind();
}

void SnifferSocket::EnablePromiscuousMode() {
   
    if (!SnifferSocket::IsInterfaceInPromiscuousMode(this->_ifname->c_str())) {
        this->TogglePromiscuousMode();
    }
}

void SnifferSocket::DisablePromiscuousMode() {

    if (SnifferSocket::IsInterfaceInPromiscuousMode(this->_ifname->c_str())) {
        this->TogglePromiscuousMode();
    }
}

bool SnifferSocket::IsLocalToLocal(uint8_t* buffer, uint32_t buffer_size) {

    return (memcmp(buffer, buffer + 6, 6) == 0) ? true : false; 
}

Message* SnifferSocket::ReceiveMessage() {

    sockaddr_ll pkt_hdr;
    pkt_hdr.sll_family = AF_PACKET;
    pkt_hdr.sll_protocol = htons(ETH_P_ALL);
    pkt_hdr.sll_ifindex = this->_interface_index;
    pkt_hdr.sll_pkttype = PACKET_OTHERHOST;
    // 1522 Bytes = Max Size of Ethernet frame (incl. VLAN-Tag)
    uint32_t buffer_size = 1522;
    uint8_t* buffer = new uint8_t[buffer_size];
    socklen_t pkt_hdr_size = sizeof(pkt_hdr);
    ssize_t msg_size = recvfrom(this->_socket_fd, buffer, buffer_size, 0,
                                (sockaddr*) &pkt_hdr, &pkt_hdr_size); 
    
    if (this->IsLocalToLocal(buffer, buffer_size)) {
        // local to local packet will be seen twice by the device
        // therefore one will be discarded.
        msg_size = recvfrom(this->_socket_fd, buffer, buffer_size, 0,
                                (sockaddr*) &pkt_hdr, &pkt_hdr_size); 
    }
    if (msg_size == -1) {
        throw Exception("Couldn't read from socket");
    }
    else if (msg_size == 0) { /* peer shut down (see man recvfrom) => nothing to do */ }

    return new Message(buffer, buffer_size, (uint32_t) msg_size);
}

SnifferSocket::~SnifferSocket() {
    
    this->DisablePromiscuousMode();
    if (this->_ifname != NULL) { delete this->_ifname; }
}

int SnifferSocket::GetInterfaceIndex(const char* ifname) {

    int if_index;

    if (SnifferSocket::IsInterfaceNameValid(ifname)) {
        int socket_fd = socket(AF_INET, SOCK_DGRAM, 0);
        // socket creation failed
        if (socket_fd == -1) {
            throw Exception(strerror(errno));
        }
        // socket created
        else {
            ifreq request;
            strncpy(request.ifr_name, ifname, IFNAMSIZ);
            // index request failed
            if (ioctl(socket_fd, SIOCGIFINDEX, &request) == -1) {
                throw Exception(strerror(errno));
            }
            else {
                if_index = request.ifr_ifindex;
            }
        }
    }
    // ifname is invalid
    else {
        throw Exception("Invalid interface name.");
    }

    return if_index;
}

bool SnifferSocket::IsInterfaceNameValid(const char* ifname) {

    return (strlen(ifname) <= IFNAMSIZ) ? true : false;
}


bool SnifferSocket::IsInterfaceInPromiscuousMode(const char* ifname) {

    bool promiscuous_mode = false;

    if (SnifferSocket::IsInterfaceNameValid(ifname)) {
        int socket_fd = socket(AF_INET, SOCK_DGRAM, 0);
        // socket creation failed
        if (socket_fd == -1) {
            throw Exception(strerror(errno));
        }
        // socket created
        else {
            ifreq request;
            strncpy(request.ifr_name, ifname, IFNAMSIZ);
            // flag request failed
            if (ioctl(socket_fd, SIOCGIFFLAGS, &request) == -1) {
                throw Exception(strerror(errno));
            }
            // evaluate received flags
            else {
                promiscuous_mode = ((IFF_PROMISC & request.ifr_flags) != 0) ? true : false;
            }
        }
    }
    // ifname is invalid
    else {
        throw Exception("Invalid interface name.");
    }

    return promiscuous_mode;
}

