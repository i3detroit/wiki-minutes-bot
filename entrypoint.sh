#!/bin/bash
if which $1; then
    exec "$@"
else
    exec python /pwb/core/pwb.py "$@"
fi