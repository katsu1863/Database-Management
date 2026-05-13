#!/bin/bash
set -e -v

echo "Creating and filling tables from HW3 solution..."
./createDatabase.sh

echo "Running..."
python3 ./main.py
