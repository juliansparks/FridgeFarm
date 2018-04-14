#!/usr/bin/env bash

NUM_ARGS=$#

if [ $NUM_ARGS -eq 0 ]; then
    echo "Too few argumnets. Exiting"
    exit 1
fi

mypy $@ 2>&1
