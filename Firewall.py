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
                    self.kill_service(external_port, service)
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

    def kill_service(self,port, service):
        if service.stop_cmd is not None:
            out = Popen(service.stop_cmd, stdout=None, shell=True)
        else:
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
                self.logger.error('Unable to find the service on this port')

    #Listening on the original port to listen to the incoming connections
    def create_proxy(self,port,service):
        try:
            #TODO Load service configuration
            sys.path.append('/root/ssproject/Filters')
            proxySocket = socket(AF_INET, SOCK_STREAM)
            proxySocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            proxySocket.bind(('',int(port)))
            proxySocket.listen(service.req_queue_size)
            #TODO Control the accept data length

            # print 'Proxy created and running on port', port
            self.logger.info('Proxy CREATED and Running on PORT '+str(port))
            while True:
                service = self.configuration.reloadService(port)
                request_sock,(clhost, clport)=proxySocket.accept()
                child_id = os.fork()
                if (child_id == 0):
                    prxy_chld_sock = socket(AF_INET, SOCK_STREAM)
                    prxy_chld_sock.connect(('', service.internal_port))

                    incoming = True
                    while incoming:
                        data = request_sock.recv(service.buffer)
                        self.logger.info("Firewall-Service:%d: Request at Proxy %s" % (port, data))

                        self.logger.info("Firewall-Service:%d: Before filter" % (port))
                        (error_msg, status) = self.applyFilterCheck(service, port, data)
                        self.logger.info("Firewall-Service:%d: After filter %s %s" % (port, status, error_msg))

                        if status is True:
                            map_port = self.port_map[port]
                            prxy_chld_sock.send(data)
                            response = prxy_chld_sock.recv(service.buffer)
                            self.logger.info("Response at Proxy " + response)
                            self.logger.info('RESPONSE from MAIN Port:' + str(map_port) + ' -> ' + str(response))
                            request_sock.send(response)
                        else:
                            self.logger.error(
                                "Firewall-Service:%d: Request failed the filter check on %s" % (port, error_msg))

                        if data == '':
                            break
                    prxy_chld_sock.close()
                    request_sock.close()
        except Exception as exc:
            handle_Exception(exc)

    def applyFilterCheck(self, service, port, data):
        if service.parser is None:
            return ("correct", True)
        else:
            pname = service.parser.attrib.get('name',None)
            parserPath = pname
            try:
                parserMod = self.filter_object(parserPath)
                data=parserMod.parse(data)
                print 'Parser returned ',data
            except Exception, err:
                self.logger.error('Firewall-Service:%d - ERROR: %s' % (port, str(err)))
                return ("correct", True)

        for filter in service.filterList:
            name = filter.attrib.get('name',None)
            if name is None:
                self.logger.info("No name attribute available for filter ")
            else:
                filter_path = name + "." + name
                #print 'Filter path: ',filter_path
                try:
                    import_filter = self.filter_object(filter_path)
                    print 'import_filter is: ',import_filter
                    obj = import_filter()
                    print 'Object is ',obj
                    res = obj.filterOut(service, data)
                    print 'Filter: ',name + res

                    if res is False:
                        error_msg = "Filter error found for " + name
                        return (error_msg, False)
                except Exception, err:
                    self.logger.error('Firewall-Service:%d - ERROR: %s' % (port, str(err)))
        return ("correct", True)

    def filter_object(self, name):
        components = name.split('.')
        print 'Components: ',components
        mod = __import__(components[0])
        print 'Mod is: ',mod
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

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
