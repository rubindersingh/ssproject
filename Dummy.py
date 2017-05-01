#!/usr/bin/env python
from socket import *
from subprocess import *
import sys
import os
import time
import threading as th
import logging as log

#service_up=Popen("python Service 50001",stdout=PIPE,stdin=None,close_fds=True, shell=True, )
#print service_up
#time.sleep(100)

def applyFilterCheck(self, service, port, data):
    for filter in service.filterList:
        name = filter.attrib.get('name', None)
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

sys.path.append('~/SoftwareSecurity/PROJECT/ssproject/Filters')

filter_path = "multi_pattern_check1.multi_pattern_check1"
import_filter = filter_object(filter_path)
obj = import_filter()
print "Hello"


