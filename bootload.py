#!/usr/bin/python3

import serial
import time
import sys

def read_bytes(filename):
    with open(filename, 'r') as fileobj:
        lines = fileobj.readlines()
        for line in lines:
            num_bytes = line[1:3]
            num_bytes = int(num_bytes, 16)
            address = int(line[3:7], 16)
            for byte in range(num_bytes):
                yield address+byte, int(line[9+byte*2: 11+byte*2], 16)


with serial.Serial('/dev/tty.usbserial-1420', 1200, timeout=1) as ser:
    
    for addr, byte in read_bytes(sys.argv[1]):
        print ("Addr: {}, byte: {}".format(hex(addr), hex(byte)))
        if (addr > 0x28FF) or (addr < 0x2800):
            print ("Skip!")
        else:
            print ("I would like to write {} {}".format(hex(addr&0xFF), hex(byte)))
            a = ser.write(bytes([addr&0xff, byte]))
            print ("Wrote {} Bytes".format(a))

    ser.close()

