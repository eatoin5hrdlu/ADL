#!/usr/bin/python -u
import liblo, sys, time

try:
    target = liblo.Address(57121)
except liblo.AddressError, err:
    print str(err)
    sys.exit()

i = 0;
while(i < 10) :
    time.sleep(10);
    liblo.send(target, "/adl", i);
    i = i + 1
