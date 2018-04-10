#!/usr/bin/env bash

echo "Running pre-commit hook"
flask test lint

if [ $? -ne 0 ]; then
 echo "Code must pass linter (flask test lint) before commit!"
 exit 1
fi
