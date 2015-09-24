#!/usr/bin/env python
import pika
import uuid
__author__ = 'David'


terminal_rpc = RemoteProcedure()

print("[x] Requesting terminal open of 'Hello World!'")
response = terminal_rpc.call("Hello World!")
print("[.] Got %r" % (response,))

