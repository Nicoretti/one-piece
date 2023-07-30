# This makefile currently only work for Linux

CXX_FLAGS = -ggdb -Wall -Werror 

SRC_DIR = ./snf/src
INCLUDE_DIR = ./snf/include

BUILD_DIR = ./out
GTEST_DIR = ./libs/gtest

all: sniffer

sniffer: prepare_build esr_lab_sniffer exception sniffer_socket
	cd $(BUILD_DIR)
	$(CXX) $(CXX_FLAGS) -I$(INCLUDE_DIR) -o $(BUILD_DIR)/sniffer $(BUILD_DIR)/esr_lab_sniffer.o $(BUILD_DIR)/exception.o $(BUILD_DIR)/message.o $(BUILD_DIR)/sniffer_socket.o $(BUILD_DIR)/pretty_printer.o

esr_lab_sniffer: prepare_build exception sniffer_socket pretty_printer
	$(CXX) $(CXX_FLAGS) -I$(INCLUDE_DIR)/ -o $(BUILD_DIR)/esr_lab_sniffer.o -c $(SRC_DIR)/esr_lab_sniffer.cpp 

exception: prepare_build $(INCLUDE_DIR)/Exception.h $(SRC_DIR)/Exception.cpp
	$(CXX) $(CXX_FLAGS) -I$(INCLUDE_DIR) -o $(BUILD_DIR)/exception.o -c $(SRC_DIR)/Exception.cpp

sniffer_socket: prepare_build $(INCLUDE_DIR)/SnifferSocket.h $(SRC_DIR)/SnifferSocket.cpp message 
	$(CXX) $(CXX_FLAGS) -I$(INCLUDE_DIR) -o $(BUILD_DIR)/sniffer_socket.o -c $(SRC_DIR)/SnifferSocket.cpp

pretty_printer: prepare_build $(INCLUDE_DIR)/PrettyPrinter.h $(SRC_DIR)/PrettyPrinter.cpp message
	$(CXX) $(CXX_FLAGS) -I$(INCLUDE_DIR) -o $(BUILD_DIR)/pretty_printer.o -c $(SRC_DIR)/PrettyPrinter.cpp

message: prepare_build $(INCLUDE_DIR)/Message.h $(SRC_DIR)/Message.cpp
	$(CXX) $(CXX_FLAGS) -I$(INCLUDE_DIR) -o $(BUILD_DIR)/message.o -c $(SRC_DIR)/Message.cpp

prepare_build:
	mkdir -p $(BUILD_DIR)
	
clean:
	rm -rf $(BUILD_DIR)
	rm -f sniffer
