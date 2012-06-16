#!/bin/bash
# This neat little script displays a full-screen image and locks your screen
# Dependencies: feh, xtrlock

feh -FZ ~/stuff/bg.jpg &
PID=$!
until xtrlock; do; done;
kill $PID
