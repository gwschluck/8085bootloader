#!/usr/bin/python3

import serial
import time
import sys

SerialPort = '/dev/tty.usbserial-1420'
BaudRate = 1200
InterByteDelay = 0.01
# Output Full 16-bit address?
FullAddress = True
# Only Used if FullAddress = 0 -- when we send 8-bit address followed by 8-bit byte
AddressMSB = 0x28
Debug = False


def read_bytes(filename):
    with open(filename, 'r') as fileobj:
        lines = fileobj.readlines()
        for line in lines:
            num_bytes = line[1:3]
            num_bytes = int(num_bytes, 16)
            address = int(line[3:7], 16)
            for byte in range(num_bytes):
                yield address+byte, int(line[9+byte*2: 11+byte*2], 16)


with serial.Serial(SerialPort, BaudRate, timeout=1) as ser:

    byte_seq = 0  # We went to print out 8 bytes at a time
    prev_addr = 0

    for addr, byte in read_bytes(sys.argv[1]):
        
        # Give user feedback
        if (prev_addr + 1) != addr:
            byte_seq = 0
            print ("")
        if byte_seq == 0:
            print (" ADDR {:04X} :".format(addr), end = '')
        if (byte_seq % 4) == 0:
            print (" ", end = '')
        print (" {:02X} ".format(byte), end = '')
        byte_seq += 1;
        if byte_seq == 16:
            byte_seq = 0
            print ("")
        prev_addr = addr;

        if Debug: 
            print ("Addr: {:04X}, byte: {:02X}".format(addr, byte))
        if not FullAddress and ((addr > ((AddressMSB<<8)|0xFF)) or (addr < (AddressMSB<<8))):
            print (" Skipping Address: {:04X}!".format(addr))
            byte_seq = 0;
        else:
            if FullAddress:
                if Debug:
                    print ("I would like to write {:02X}".format((addr&0xFF00)>>8))
                a = ser.write(bytes([((addr&0xff00)>>8)]))
                time.sleep(InterByteDelay)
            else:
                a = 0

            if Debug:
                print ("I would like to write {:02X}".format(addr&0xFF))
            a += ser.write(bytes([addr&0xff]))
            time.sleep(InterByteDelay)
            if Debug:
                print ("I would like to write {:02X}".format(byte))
            a += ser.write(bytes([byte]))
            time.sleep(InterByteDelay)
            if Debug:
                print ("Wrote {} Bytes".format(a))

    ser.close()

    print ("\n")

