#!/bin/bash

cd "$(dirname "$0")"

source bin/python-3/bin/activate

python bin/run_resolve.py
