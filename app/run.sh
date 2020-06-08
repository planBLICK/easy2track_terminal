#!/bin/bash

cleanup ()
{
kill -s SIGTERM $!
exit 0
}
trap cleanup SIGINT SIGTERM

if [ ! -f /home/pi/easy2track/app/login_data.json ]; then
    echo "No login-credentials found, asking now..."
    /usr/bin/python3 /home/pi/easy2track/app/init_app.py
fi


COMMAND="/usr/bin/python3 /home/pi/easy2track/app/main.py -u=$1 -p=$2"
echo "Starting"
while true ; do
  $COMMAND
  echo -e "Exited with status $?"
  echo "Restarting"
done