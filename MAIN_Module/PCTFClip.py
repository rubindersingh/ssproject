#!/usr/bin/env python
from socket import *
from subprocess import *
import sys
import os
import time
import threading as th
import logging as log

class Clippers:
    port_map={}
    #Initializing the necessary variables from CONFIG file
    def __init__(self,config,message):
        #Preparing the Logger for the Messages
        self.logger = log.getLogger('Clippers')
        self.logger.setLevel(log.DEBUG)

        #File handler which creates a Fresh File everytime it is run
        self.handler = log.FileHandler(message,mode='a')
        self.handler.setLevel(log.DEBUG)

        #Formatter to specify the format of the LOG messages
        self.formatter = log.Formatter('%(levelname)s %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

        #Extracting the CONFIG parameters
        for line in file(config):
            if len(line)!=0:
                split_line=line.split()
                if '#' in split_line[0]:
                    continue
                elif 'Service' in split_line[0]:
                    self.port_map[int(split_line[1])]=int(split_line[2])
                elif 'buf' in split_line[0]:
                    self.buffer=int(split_line[1])
                elif 'exec' in split_line[0]:
                    self.command=str(split_line[1])
                elif 'file' in split_line[0]:
                    self.path=str(split_line[1])
        self.logger.info('Loaded the Config File')
        #self.logger.info(self.port_map + self.buffer + self.command+ self.path +'\n')

    def map_services(self):
        self.fork_process=[]

        #Mapping the existing services to the Mapped ports
        for port in self.port_map:
            #print 'Forking for port ',port
            PID_forked=os.fork()
            if (PID_forked==0):
                try:
                    mapped_port=self.port_map[port]
                    service_up=Popen([self.command,self.path, str(mapped_port)],stdout=PIPE,stdin=None,close_fds=True)

                    #print 'Mapped the service at port %d to %d\n' % (port,mapped_port)
                    self.logger.info('Mapped the service at port %d to %d\n' % (port,mapped_port))

                    #Killing the Existing Service running on PORT
                    self.kill_service(port)
                    time.sleep(2)

                    #Starting the PROXY on the original port
                    self.create_proxy(port)

                    #Kill the child and preventing it from entering the loop
                    sys.exit(0)
                except Exception as exc:
                    handle_Exception(exc)
            else:
                print 'The child forked is ',PID_forked
                self.fork_process.append(PID_forked)

    def kill_service(self,port):
        #The PID parameter is the 2nd argument in the output of lsof
        #Killing the Running Service, 9 stands for signal.SIGKILL
        out=Popen(["lsof","-P","-i"],stdout=PIPE)
        details=Popen(["grep",str(port)],stdin=out.stdout,stdout=PIPE)
        proc_details=details.stdout.read()

        if len(proc_details)!=0:
            current_PID=proc_details.split()[1]
            self.logger.info('PID of Original Service running at port '+str(port)+' is '+str(current_PID))
            os.kill(int(current_PID),9)

            #print 'Killed the Service running at port '+str(port)
            self.logger.info('Killed the Service running at port '+str(port))
        else:
            print 'Unable to find the service on this port'

    #Listening on the original port to listen to the incoming connections
    def create_proxy(self,port):
        try:
            proxySocket = socket(AF_INET, SOCK_STREAM)
            proxySocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            proxySocket.bind(('',int(port)))
            proxySocket.listen(5)

            #print 'Proxy created and running on port', port
            self.logger.info('Proxy CREATED and Running on PORT '+str(port))
            while True:
                request_sock,(clhost, clport)=proxySocket.accept()
                data      = request_sock.recv(self.buffer)
                attributes= data.split()[1:]
                param     = ''.join(str(word) for word in attributes)
                #print 'Message Received at PROXY Port: ',param
                self.logger.info('REQUEST at PROXY Port:' + str(port) + ' -> ' + str(param))
                map_port=self.port_map[port]
                response=self.proxy_client(param,map_port)

                self.logger.info('RESPONSE from MAIN Port:' + str(map_port) + ' -> ' + str(response))
                request_sock.send(response)
                request_sock.close()
        except Exception as exc:
            handle_Exception(exc)

    def proxy_client(self,arguments,mapped_port):
        try:
            prxy_chld_sock = socket(AF_INET, SOCK_STREAM)
            prxy_chld_sock.connect(('',int(mapped_port)))

            prxy_chld_sock.send(str(arguments))
            response=prxy_chld_sock.recv(self.buffer)

            prxy_chld_sock.close()
            return response
        except Exception as exc:
            handle_Exception(exc)

    def alive_threads(self):
        print 'The Active Threads are:'
        for thread in th.enumerate():
            print thread.getName()
        return th.active_count()

def handle_Exception(ex):
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print message

clip=Clippers('proxy.config','messages.log')
clip.map_services()
clip.fork_process
