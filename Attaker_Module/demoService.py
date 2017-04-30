#!/usr/bin/env python
from socket import *
import sys
import os



for port in [10001,10002,10003]:
    
    
    pid= os.fork()
    if(pid==0):
        
        sock=AF_INET
        stream=SOCK_STREAM

        stream_sock=socket(sock, stream)
        stream_sock.bind(('',port))
        stream_sock.listen(5)
        print 'Service Started'
        while True:
            client, (clienthost, clientport) = stream_sock.accept()
            print "\n\n************** Request at ",port
            msg = "SERVER Says: " + client.recv(65536)

            print msg
            
            client.send("Request received at " + str(port))
            client.close()
        
    else:
        print "Service started at", port
        
        
        
"""

 ps -ef | grep "python service" 

"""
