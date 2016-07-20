#!/bin/bash
echo "To:peter.reintjes@ncmls.org" >mail.text
echo "From:peter@huxley" >>mail.text
echo "Subject: Here is my IP address" >>mail.text
echo "" >>mail.text
ifconfig >>mail.text
ssmtp peter.reintjes@ncmls.org <mail.text

