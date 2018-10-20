#!/usr/bin/env python3

import zmq
import random
import sys
import time

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

while True:
    topic = 'event'
    messagedata = random.randrange(1,215) - 80
    print ("%{} %{}".format(topic, messagedata))
    socket.send_string("{} {}".format(topic, messagedata))
    time.sleep(1)
