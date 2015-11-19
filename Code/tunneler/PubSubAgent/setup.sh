#!/usr/bin/env bash
SETUP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SETUP_DIR
cd ..
sudo cp -rf PubSubAgent /var/opt/
