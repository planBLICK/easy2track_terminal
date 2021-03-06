#!/bin/sh

cd /usr/bin/
./git clone "https://github.com/planBLICK/easy2track_terminal.git" "/home/pi/easy2track/" 2> /dev/null || (cd "/home/pi/easy2track/"; git fetch; git reset --hard origin/live;  git pull; )
chmod +x /home/pi/easy2track/setup.sh
chmod +x /home/pi/easy2track/app/run.sh

sudo cp /home/pi/easy2track/easy2track_terminal_update.service /etc/systemd/system
sudo systemctl daemon-reload
systemctl status easy2track_terminal_update.service
sudo systemctl enable easy2track_terminal_update.service
sudo systemctl start easy2track_terminal_update.service

sudo cp /home/pi/easy2track/easy2track_terminal.service /etc/systemd/system
sudo systemctl daemon-reload
systemctl status easy2track_terminal.service
sudo systemctl enable easy2track_terminal.service
sudo systemctl start easy2track_terminal.service
sleep 3