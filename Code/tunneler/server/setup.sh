#!/usr/bin/env bash
SETUP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SETUP_DIR
cd ..
sudo cp -rf server /var/opt/
runOnReboot="sudo update-rc.d /var/opt/server/on_startup.sh defaults"
sudo cp -rf /var/opt/server/on_startup.sh /etc/init.d/
sudo chmod +x /etc/init.d/on_startup.sh
sudo update-rc.d on_startup.sh defaults
sudo update-rc.d on_startup.sh start defaults
sudo update-rc.d on_startup.sh stop defaults
python /var/opt/server/Main.py &
