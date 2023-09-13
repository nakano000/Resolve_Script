#!/bin/bash

cd `dirname $0`
SCRIPT_DIR=`pwd`

export PYTHONHOME=$SCRIPT_DIR/bin/python-3.10.11

bin/python-3.10.11/bin/python3 bin/run_fusion.py

exit 0
