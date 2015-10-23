#!/usr/bin/env bash
SETUP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SETUP_DIR
cd ..
cp -rf server_agent /var/opt/
runOnReboot="crontab -u '/var/opt/server_agent/setOnStartUp.sh'"
START_SERVER="python /var/opt/server_agent/Main.py"
eval $START_SERVER