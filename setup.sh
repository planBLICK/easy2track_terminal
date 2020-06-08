#!/bin/sh

cd /usr/bin/
./git clone "https://github.com/planBLICK/easy2track_terminal.git" "/home/pi/easy2track/" 2> /dev/null || (cd "/home/pi/easy2track/" ; git pull)
