#!/usr/bin/sh
IP1=`curl -s http://checkip.amazonaws.com`
echo "Updatin $IP1 in settings file"
sed -i 's/ipxxxx/'".iksaan.com\",\"$IP1"'/' iksaan/settings.py

