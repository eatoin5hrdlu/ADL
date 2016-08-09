#!/usr/bin/python -u
import sys, os, time, socket, subprocess
from os  import popen
import RPi.GPIO as GPIO

button   =  [
              4,  # B1  GPIO4  (Header pin 7)
              14, # B2  GPI14  (Header pin 8)
              17, # B3  GPIO17 (Header pin 11)
              27, # B4  GPI27  (Header pin 13)
              22, # B5  GPIO22 (Header pin 15)
              10, # B6  GPIO10 (Header pin 19)
               9, # B7  GPIO09 (Header pin 21)
              11, # B8  GPIO11 (Header pin 23)
               8, # B9  GPIO8  (Header pin 24)
              25  # B10 GPIO25 (Header pin 22)
               ]

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

reset = False
recent =  0
summer = 0
fall = 0

def  summerbuttons() :
    gd = GPIO.input(button[0]) or GPIO.input(button[2]) or GPIO.input(button[4])
    print("sb "+str(gd))
    return not gd

def  fallbuttons ():
    gd = GPIO.input(button[1]) or GPIO.input(button[3]) or GPIO.input(button[5])
    print("fb "+str(gd))
    return not gd


def seasonal() :
    global recent
    global reset
    global summer
    global fall
    now = time.time()
    if ( now - recent < 2):
        return
    if (not reset and not summerbuttons() and not fallbuttons()): # Buttons up
        reset = True
        recent = now
        return
    
    if (reset and summerbuttons()) :
        summer = summer + 1
        print("summer = "+str(summer))
        if (summer > 2) :
            summer = 0
            fall = 0
            reset = True
            fp = open('season.txt','w')
            print(fp,"summer\n")
            print("summer\n")
            close(fp)
            time.sleep(2)
        reset = False
    elif (reset and fallbuttons()) :
        fall = fall + 1
        print("fall = "+str(fall))
        if (fall > 2) :
            summer = 0
            fall = 0
            reset = True
            fp = open('season.txt','w')
            print(fp,"fall\n")
            print("fall\n")
            close(fp)
            time.sleep(2)
        reset = False
    else :
        reset = True  # Buttons released

    recent = now
    

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme


for i in button:
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

reset = True
proc = None
proc = subprocess.Popen(['/usr/bin/aplay','02c.wav'])

while 1:
    seasonal()
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


