#!/usr/bin/env python
from socket import *
import sys
import os
import signal

sock=AF_INET
stream=SOCK_STREAM

stream_sock=socket(sock, stream)
stream_sock.bind(('',50002))
stream_sock.listen(5)
print 'Service Started'
while True:
    client, (clienthost, clientport) = stream_sock.accept()
    child_id = os.fork()
    if child_id == 0:
        mypid = os.getpid()
        count = 0
        while True:
            data = client.recv(1024)
            count+=1
            print data, len(data), data[-1].encode("hex")
            msg = "SERVER Says: " + data
            client.send(msg)
            if data == '' or count==4:
                break
        print "Closing connection"
        client.shutdown(1)
        client.close()
        os.kill(mypid, signal.SIGTERM)
        sys.exit(0)
