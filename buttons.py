#!/usr/bin/python -u
import sys, os, time, socket, subprocess
from os  import popen
import RPi.GPIO as GPIO

button   =  [ 18, # GPIO0  (Header pin 12)
              23, # GPIO1  (Header pin 16)
              4,  # GPIO2  (Header pin 7)
              17, # GPIO17 (Header pin 11)
               8, # GPIO8  (Header pin 24)
              22, # GPIO22 (Header pin 15)
              10, # GPIO10 (Header pin 19)
               9, # GPIO11 (Header pin 21)
              11, # GPIO9  (Header pin 23)
               7 ]# GPIO7  (Header pin 26)

files = [ "01c.wav",
          "02c.wav",
          "03c.wav",
          "04c.wav",
          "05c.wav",
          "06c.wav",
          "07c.wav",
          "08c.wav",
          "1ac.wav",
          "19c-old.wav"];

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

for i in button:
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

reset = True
proc = None

while 1:
    allup = True
    for i in range(len(button)) :
        if ( GPIO.input(button[i]) == 0 ) :
            allup = False
    if (allup) :
        reset = True;
    for i in range(len(button)) :
        if ( reset and ( GPIO.input(button[i]) == 0 ) ) :
            print("button pressed: "+str(i))
            if (proc != None) :
                proc.terminate()
            fname = '/home/pi/src/ADL/'+files[i]
            proc = subprocess.Popen(['/usr/bin/aplay',fname])
            time.sleep(1)
            reset = False


