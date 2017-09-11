#!/bin/bash

{ airodump-ng wlan0mon 2>> output.txt; } &
PID=$!

sleep 5

kill -TERM $PID
cat output.txt
