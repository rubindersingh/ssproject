#!/usr/bin/env python
from subprocess import *
import os
import time
import sys
#11002 12002 13002 6000 7000 8000
#11002 12002 13002

ports=sys.argv[1:]
map_ports=map(int, ports)
#print map_ports

for port in map_ports:
    time.sleep(1)
    try:
        out=Popen(["lsof","-P","-i"],stdout=PIPE)
        proc_details=check_output(["grep",str(port)],stdin=out.stdout)
        #The PID parameter is the 2nd argument in the output of lsof
        current_PID=proc_details.split()[1]
        print 'PID of Current Service', current_PID
        os.kill(int(current_PID),9)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message
