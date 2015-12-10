@echo off
cls
python --version 2>NUL
if errorlevel 1 goto nopythonerror
easy_install pip
pip install pika
.\rabbitmq-plugins.bat enable rabbit_management
.\rabbitmq-plugins.bat enable rabbit_web_stomp
.\rabbitmq-plugins.bat enable rabbit_presence_exchange

exit 0

:nopythonerror
echo No installation of Python detected
exit 1