#!/bin/bash

# Kill the process using the port 2000 if any
echo 'Cleaning up...'

PID="$(sudo netstat -pl | grep :2000 | awk  {'print $7'} | awk -F '/' {'print $1'})"

if [ -n "${PID}" ]; then
	echo "Killing ${PID}"
	sudo kill -9 "${PID}"
fi

echo "Starting server..."
WLAN_IP=$(ip addr show wlan0 | grep -Po 'inet \K[\d.]+')
echo "$WLAN_IP"
python /home/pi/WifiTruckServerApplication/wifi_truck_server.py "$WLAN_IP"
echo "Last line in start script"
