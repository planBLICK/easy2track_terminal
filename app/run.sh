#!/bin/bash

cleanup ()
{
kill -s SIGTERM $!
exit 0
}
trap cleanup SIGINT SIGTERM


COMMAND="/usr/bin/python3 /home/pi/easy2track/app/main.py -u=$1 -p=$2"
echo "Starting"
while true ; do
  $COMMAND
  echo -e "Exited with status $?"
  echo "Restarting"
done