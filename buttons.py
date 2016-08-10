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

state = 0
idle = 0
summercount = 1
fallcount = 2

recent =  time.time()
summer = 0
fall = 0

def resetstate(now) :
    global state, idle, summer, fall, recent
    state = idle
    summer = 0
    fall = 0
    recent = now
    
def  checkCount() :
    global recent
    global state, idle, summercount, fallcount
    global summer, fall
    now = time.time()
    if (recent > now) : # overflow
        resetstate(now)
        return
    if (now - recent < 2) : # not yet
        return
    if (now - recent > 60) : # timed out
        resetstate()
        return
    # Check for the two secret button patterns
    sc = not (GPIO.input(button[0]) or GPIO.input(button[2]) or GPIO.input(button[4]))
    fc = not (GPIO.input(button[1]) or GPIO.input(button[3]) or GPIO.input(button[5]))
    if (state == idle) :
        if (sc) :
            summer = 0
            state = summercount
            recent = now
        elif (fc) :
            fall = 0
            state = fallcount
        recent = now
    if (sc and state==summercount) :
        summer = summer + 1
        recent = now
    if (fc and state==fallcount) :
        fall = fall + 1
        recent = time.time()
    if (sc and state=fallcount) :
        resetstate(now)
    if (fc and state=summercount) :
        resetstate(now)
    if (sc and summercount > 2):
        fp = open('season.txt','w')
        print(fp,"summer\n")
        print("summer\n")
        close(fp)
        resetstate(now)
    if (fc and fallcount > 2):
        fp = open('season.txt','w')
        print(fp,"fall\n")
        print("fall\n")
        close(fp)
        resetstate(now)

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme


for i in button:
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

reset = True
proc = None
proc = subprocess.Popen(['/usr/bin/aplay','02c.wav'])

while 1:
    checkCount()
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


