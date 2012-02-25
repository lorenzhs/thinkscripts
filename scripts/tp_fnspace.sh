#!/bin/bash
# This goes to /etc/acpi/
kill -SIGUSR1 `cat /tmp/sc.pid`
