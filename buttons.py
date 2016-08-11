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

fallfiles = [ 
"01Hooded-Merganser.wav",
"02Red-bellied-Woodpecker.wav",
"03Belted-Kingfisher.wav",
"04Yellow-rumped-Warbler.wav",
"05White-throated-Sparrow.wav",
"06Red-shouldered-Hawk.wav",
"07Yellow-bellied-Sapsucker.wav",
"08Carolina-Wren.wav",
"09Northern-Cardinal.wav",
"10Spring-Peeper.wav"
    ];

summerfiles = [
"01Belted-Kingfisher.wav",
"02Great-Blue-Heron.wav",
"03Gray-Catbird.wav",
"04Gray-Treefrog.wav",
"05Bullfrog.wav",
"06Red-shouldered-Hawk.wav",
"07Green-Heron.wav",
"08Song-Sparrow.wav",
"09Green-Treefrog.wav",
"10Cicada-Hydroglyphica.wav"
];


state = 0 # state changes, the next three are constant states
idle = 0
summercount = 1
fallcount = 2

recent =  time.time()
summer = 0
fall = 0

summerseason = 3
fallseason   = 4
season = 3

def setseason() :
    global season, summerseason, fallseason
    sf = open('season.txt','r')
    ses = sf.read().split()[0]
    sf.close()
    if ((ses == 'summer' and season == summerseason) or (ses == 'fall' and season == fallseason)) :
        return
    if (ses == 'summer') :
        season = summerseason
    elif (ses == 'fall') :
        season = fallseason
    

def resetstate(now) :
    global state, idle, summer, fall, recent
    state = idle
    summer = 0
    fall = 0
    recent = now
    
def  checkCount() :
    global recent
    global state, idle, summercount, fallcount
    global season, summer, fall, summerseason, fallseason
    now = time.time()
    if (recent > now) : # overflow
        print("overflow")
        resetstate(now)
        return
    if (now - recent < 2) : # not yet
        return
    if (now - recent > 60) : # timed out
        print("timeout")
        resetstate(now)
        sf = open('season.txt','r')
        print("SEASON: ")
        ses = sf.read().split()[0]
        sf.close()
        print(ses)
        if ((ses == 'summer' and season == summerseason) or (ses == 'fall' and season == fallseason)) :
            return
        if (season == summerseason) :
            season = fallseason
        else :
            season = summerseason
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
    if (sc and state==fallcount) :
        resetstate(now)
    if (fc and state==summercount) :
        resetstate(now)
    if (sc and summer > 2):
        fp = open('season.txt','w')
        fp.write("summer\n")
        fp.close()
        resetstate(now)
    if (fc and fall > 2):
        fp = open('season.txt','w')
        fp.write("fall\n")
        fp.close()
        resetstate(now)

def allup() :
    global button
    someDown = True;
    while(someDown) :
        for i in range(len(button)) :
            if (GPIO.input(button[i]) == 0) :
                break
        someDown = False

        
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme


for i in button:
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

reset = True
proc = None
#proc = subprocess.Popen(['/usr/bin/aplay','02c.wav'])

setseason()
while 1:
    allup = True
    for i in range(len(button)) :
        if ( GPIO.input(button[i]) == 0 ) :
            allup = False
    if (allup) :
        reset = True
    firsttime = True
    for i in range(len(button)) :
        if ( reset and ( GPIO.input(button[i]) == 0 ) and firsttime ) :
            firsttime = False
            checkCount()
            allup()
            if (proc != None) :
                proc.terminate()
                proc = None
            subprocess.Popen(['/usr/bin/pkill','-9','/usr/bin/aplay'])
            time.sleep(0.2)
            if (season == summerseason):
                fname = '/home/pi/src/ADL/summer/'+summerfiles[i]
            elif (season == fallseason):
                fname = '/home/pi/src/ADL/fall/'+fallfiles[i]
            print(" PLAYING: " + fname)
            proc = subprocess.Popen(['/usr/bin/aplay',fname])
            time.sleep(1.0)
            reset = False
                


