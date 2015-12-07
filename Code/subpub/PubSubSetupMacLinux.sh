#!/bin/bash

clear
{
    python -c 'import sys; print(sys.version_info[:])'
} &> /dev/null
if [ "$?" != "0" ]; then
        echo 'No python installation found, please install python and try again';
        exit;
fi

{
easy_install pip
pip install pika
./rabbitmq-plugins enable rabbitmq_management
./rabbitmq-plugins enable rabbitmq_web_stomp
./rabbitmq-plugins enable rabbit_presence_exchange
} &> /dev/null