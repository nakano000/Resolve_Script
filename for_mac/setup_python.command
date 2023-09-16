#!/bin/bash

cd `dirname $0`

python3 -m venv bin/python-3
source bin/python-3/bin/activate
pip install -r requirements.txt
