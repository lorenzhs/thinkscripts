#!/bin/zsh
# This neat little script displays a full-screen image and locks your screen
# Dependencies: feh, xtrlock

FILES=( ~/stuff/backgrounds/*(.) )
feh -FZ $FILES[$RANDOM%$#FILES+1] &
PID=$!
until xtrlock; do; done;
kill $PID
