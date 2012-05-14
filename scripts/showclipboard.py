#!/usr/bin/env python
# license: CC0
# Originally written by Timo Paulssen
# Check out his setup instructions at http://wakelift.de/posts/zoom/
# tl;dr: You will need to add tp_fnspace.sh to /etc/acpi and tp_fnspace
# to /etc/acpi/events. If it does not work, READ TIMO'S BLOG POST!
# Dependencies: nomeata's Screen Message (sm), acpid, xclip, python

import signal
import os
import sys
import math
from subprocess import Popen, PIPE

def check_pid(pid):
    try: os.kill(pid, 0)
    except OSError: return False
    else: return True

def check_output(cmdparts, text=None):
     proc = Popen(cmdparts, stdout=PIPE, stdin=PIPE)
     out = proc.communicate(text)[0]
     proc.wait()
     return out

def par(text):
    # Characters are nearly twice as high as wide, screens 1.5 times wider than high
    # So sqrt(numchars) characters per line would give you something that is nearly two times higher
    # than wide. Making it wider by a factor of 2.1 should work out for most screens.
    maxlen = max(15, int(2.1*math.sqrt(len(text))))
    call = ['par', str(maxlen)]
    return check_output(call, text)[:-1]

def do_sc(signum, frame):
    text = check_output(['xclip', '-o'])
    text = par(text)
    check_output(['sm', '-'], text)

signal.signal(signal.SIGUSR1, do_sc)

try:
    with open('/tmp/sc.pid', 'r') as pidfile:
        pid = pidfile.read()
    if check_pid(int(pid)):
        print 'sc already running at %s' % pid
        sys.exit(1)
except IOError: pass

with open('/tmp/sc.pid', 'w') as pidfile:
    pidfile.write(str(os.getpid()))

try: 
    while True: signal.pause()
finally:
    os.unlink('/tmp/sc.pid')
