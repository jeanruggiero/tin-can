#!/bin/bash
# This script contains the commands to set up a raspberry pi running Debian buster as a webserver

# Install influxdb
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/os-release
echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

# These commands may need to be re-ordered...
sudo apt-get update && sudo apt-get install influxdb
sudo systemctl unmask influxdb.service
sudo systemctl start influxdb

# Install python, pip, and virtualenv
apt install python3 pip3 virtualenv

# Create virtual environment
virtualenv venv

# Activate virtual environment
source venv/bin/activate
python -m pip install -r requirements.txt
