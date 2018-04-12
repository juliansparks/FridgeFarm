#!/usr/bin/env bash

echo "Running pre-push hook"
flask test

if [ $? -ne 0 ]; then
    echo "====================================="
    echo "Code must pass all tests before push!"
    exit 1
fi
