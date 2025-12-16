#!/bin/bash

python << EOF
import os
import sys

if 'PWB_USERNAME' not in os.environ:
    sys.exit()

with open("/tmp/pwb-password.py", "at") as passfile:
    if 'PWB_PASSWORD' in os.environ:
        print(f"('i3detroit', {os.environ['PWB_USERNAME']!r}, {os.environ['PWB_PASSWORD']!r})", file=passfile)
    if 'PWB_BOTNAME' in os.environ and 'PWB_BOTPASS' in os.environ:
        print(f"('i3detroit', {os.environ['PWB_USERNAME']!r}, BotPassword({os.environ['PWB_BOTNAME']!r}, {os.environ['PWB_BOTPASS']!r}))", file=passfile)

EOF

if which $1 > /dev/null; then
    exec "$@"
else
    exec python /pwb/core/pwb.py "$@"
fi