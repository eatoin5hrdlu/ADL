#!/usr/bin/python -u
import RPi.GPIO as GPIO
import liblo, sys, time

buttons  =  [ 0,  # GPIO0  (Header pin 3)
              1,  # GPIO1  (Header pin 5)
              4,  # GPIO2  (Header pin 7)
              17, # GPIO17 (Header pin 11)
              21, # GPIO21 (Header pin 13)
              22, # GPIO22 (Header pin 15)
              10, # GPIO10 (Header pin 19)
               9, # GPIO11 (Header pin 21)
              11, # GPIO9  (Header pin 23)
               7 ]# GPIO7  (Header pin 26)

# Set up OSC port
try:
    target = liblo.Address(57121)
except liblo.AddressError, err:
    print str(err)
    sys.exit()

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

for i in buttons:
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

reset = True;
while 1:
    allup = True
    for i in range(len(buttons)) :
        if ( GPIO.input(button[i]) == 0 ) :
            allup = False
    if (allup) :
        reset = True;
    for i in range(len(buttons)) :
        if ( reset and ( GPIO.input(button[i]) == 0 ) ) :
            liblo.send(target, "/adl", i)
            time.sleep(2)
            reset = False
