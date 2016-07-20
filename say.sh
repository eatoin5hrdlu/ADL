#!/bin/bash
sleep $1

echo "The I P address for cooveeay is" > message
ifconfig eth0 | grep -o "addr:[^ ]*" | sed s/addr:// | sed s/\\./\ dot\ /g >>message
amixer sset PCM,0 100%
exit 0
for v in slt kal kal16 awb rms slt
do
flite -s duration_stretch=1.2 -voice $v message
done




