#!/bin/bash

python -c "import os; print(repr(('i3detroit', os.getenv('PWB_USERNAME'), os.getenv('PWB_PASSWORD'))))" >> /tmp/pwb-password.py

if which $1; then
    exec "$@"
else
    exec python /pwb/core/pwb.py "$@"
fi