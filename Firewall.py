#!/usr/bin/env python
from socket import *
from subprocess import *
import sys
import os
import time
import threading as th
import logging as log

from re import search

import Configuration as conf

class Firewall:
    port_map={}
    #Initializing the necessary variables from CONFIG file
    def __init__(self,configFilePath,logFilePath):
        #Preparing the Logger for the Messages
        self.logger = log.getLogger('Clippers')
        self.logger.setLevel(log.DEBUG)

        #File handler which creates a Fresh File everytime it is run
        self.handler = log.FileHandler(logFilePath,mode='a')
        self.handler.setLevel(log.DEBUG)

        #Formatter to specify the format of the LOG messages
        self.formatter = log.Formatter('%(levelname)s %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

        #Extracting the CONFIG parameters
        self.configuration = conf.Configuration(configFilePath)
        self.logger.info('Loaded the Config File')
        #self.logger.info(self.port_map + self.buffer + self.command+ self.path +'\n')

    def map_services(self):
        self.fork_process=[]

        #Mapping the existing services to the Mapped ports
        for port in self.configuration.services:
            service = self.configuration.getService(port)
            internal_port = service.internal_port
            external_port = service.external_port
            self.port_map[external_port] = internal_port

            #print 'Forking for port ',port
            PID_forked=os.fork()
            if (PID_forked==0):
                try:
                    service_up = Popen(service.start_cmd,stdout=PIPE,stdin=None,close_fds=True, shell=True)
                    print service_up
                    #print 'Mapped the service at port %d to %d\n' % (port,mapped_port)
                    self.logger.info('Mapped the service at port %d to %d\n' % (external_port,internal_port))

                    #Killing the Existing Service running on PORT
                    self.kill_service(external_port)
                    time.sleep(2)

                    #Starting the PROXY on the original port
                    self.create_proxy(external_port, service)

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
    def create_proxy(self,port,service):
        try:
            #TODO Load service configuration
            sys.path.append('~/SoftwareSecurity/PROJECT/ssproject/Filters')
            self.buffer = 65536
            proxySocket = socket(AF_INET, SOCK_STREAM)
            proxySocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            proxySocket.bind(('',int(port)))
            proxySocket.listen(5)
            #TODO Control the accept data length
            MAX_PAYLOAD = 66000

            # print 'Proxy created and running on port', port
            self.logger.info('Proxy CREATED and Running on PORT '+str(port))
            while True:
                request_sock,(clhost, clport)=proxySocket.accept()

                data = ""
                while True:
                    recv = request_sock.recv(self.buffer)
                    if recv is None:
                        break
                    else:
                        data = data + recv

                """print "Data at Proxy ", data
                attributes= data.split()[1:]
                param     = ''.join(str(word) for word in attributes)
                #print 'Message Received at PROXY Port: ',param
                self.logger.info('REQUEST at PROXY Port:' + str(port) + ' -> ' + str(param))"""

                if len(data) > MAX_PAYLOAD:
                    self.logger.info("Request Data Size Overflown")
                    status = False
                else:
                    (error_msg, status) = self.applyFilterCheck(service, port, data)

                if status is True:
                    map_port=self.port_map[port]
                    response=self.proxy_client(data,map_port)
                    print "Response at Proxy ", response
                    self.logger.info('RESPONSE from MAIN Port:' + str(map_port) + ' -> ' + str(response))
                    request_sock.send(response)
                    request_sock.close()
                else:
                    self.logger.info("Request failed the filter check on "+error_msg)
        except Exception as exc:
            handle_Exception(exc)

    def applyFilterCheck(self, service, port, data):
        for filter in service.filterList:
            name = filter.attrib.get('name',None)
            if name is None:
                self.logger.info("No name attribute available for filter ")
            else:
                filter_path = name + "." + name
                import_filter = self.filter_object(filter_path)

                obj = import_filter()
                res = obj.filterOut(service, data)

                if res is False:
                    error_msg = "Filter error found for " + name
                    return (error_msg, False)
        return ("correct", True)

    def filter_object(name):
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def proxy_client(self,data,mapped_port):
        try:
            prxy_chld_sock = socket(AF_INET, SOCK_STREAM)
            prxy_chld_sock.connect(('',int(mapped_port)))

            prxy_chld_sock.send(data)
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

firewall=Firewall('config.xml','requests.log')
firewall.map_services()
