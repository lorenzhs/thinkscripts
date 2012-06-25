#!/bin/zsh
# This neat little script displays a random image from a folder in fullscreen and locks your screen
# Originally by Timo - https://github.com/timo
# Dependencies: feh, xtrlock

# Make sure you change this to a suitable location on your machine!
FOLDER=~lorenz/stuff/backgrounds/

# This part is machine-independent, no need to change it
feh -zFZ $FOLDER &
PID=$!
until xtrlock; do; done;
kill $PID
