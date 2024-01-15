#!/usr/bin/env bash

sudo chown -R ubuntu:ubuntu ~/pythonprojeckdjango
#python -m venv myenv
virtualenv /home/ubuntu/pythonprojeckdjango/venv
source /home/ubuntu/pythonprojeckdjango/venv/bin/activate
pip install -r /home/ubuntu/pythonprojeckdjango/requirements.txt