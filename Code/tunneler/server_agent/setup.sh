#!/usr/bin/env bash
SETUP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SETUP_DIR
cd ..
cp -rf server_agent /var/opt/
runOnReboot="sudo update-rc.d /var/opt/server_agent/on_startup.sh defaults"
cp -rf /var/opt/server_agent/on_startup.sh /etc/init.d/
sudo chmod +x /etc/init.d/on_startup.sh
sudo update-rc.d on_startup.sh defaults
sudo update-rc.d on_startup.sh start defaults
sudo update-rc.d on_startup.sh stop defaults
python /var/opt/server_agent/Main.py