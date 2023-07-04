#!/usr/bin/env bash
# exit on error
set -o errexit

apt install python3.10-full
pip install --upgrade pip
pip install -r requirements.txt
poetry install