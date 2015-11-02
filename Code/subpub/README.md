#PubSub:
    This class is used as an intemediary between RabbitMQ and any client. This project can be though of as a further
    abstraction/extension of the existing pika library used to communicate with RabbitMQ. That is to say, this class
    faciliates communication, simplifying what could result in lines of repetitious and cumbersome operations into a 
    few lines of code. This class's usage was insipired by PubNub.
    
    In addition to serving as a further abstraction of existing technologies, this project also introduces ability to keep track     of who is entering and exiting the channel. 

##Installation:
    1) There must exist an installation of Python, in order to download visit https://www.python.org/downloads/ 
    (PYTHON CLIENT ONLY)
    2) There must exist an installation of RabbitMQ, in order to download visit https://www.rabbitmq.com/download.html
    
    Python Client
    3) Windows: Configure the PYTHON environment variable by going to My Computer('This PC' on Windows 8 and up) -> 
    Properties -> Advanced system settings -> Under the Advanced tab, click "Environment Variables..." -> Under 
    "system variables" click "New..." -> enter the path to your Python installation (for example 
    "C:\Program Files\Python 3.5\") -> click "OK" -> select "PATH" and click "Edit..." -> enter ";%PYTHON%" 
    at the end (where PYTHON is what you chose to name the system variable) -> click "OK"
       OSX: PubSub is compatible with the default installation of Python
    4) Windows: Configure the PYTHON_SCRIPTS environment variable by going to My Computer('This PC' on Windows 8 and up) 
    ->  Properties -> Advanced system settings -> Under the Advanced tab, click "Environment Variables..." -> Under 
    "system variables" click "New..." -> enter the path to your Python scripts (for example 
    "C:\Program Files\Python 3.5\Scripts") -> click "OK" -> select "PATH" and click "Edit..." -> enter 
    ";%PYTHON_SCRIPTS%" at the end (where PYTHON_SCRIPTS is what you chose to name the system variable) -> 
    click "OK"
       OS X: This should already be configured
    5) Pika must be installed, in order to do so, launch the terminal/command line and enter pip install pika OR 
    easy_install pika
    6) Download pubsub.py and place the file under your Python installations /Libs folder
    7) In the client implementing the class, simply import the pubsub.py class

    Javascript:
    3) Place the pubsub.js file anywhere on the development computer
    4) Simply import the pubsub.js file by use of the <script> tags in an HTML file

##Running:

##TODO:
    - Configuration script for the RabbitMQ environment that includes automatic set-up of the necessary plugins.
    - Faciliate installation of pubsub.py
