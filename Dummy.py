#!/usr/bin/env python
from socket import *
from subprocess import *
import sys
import os
import time
import threading as th
import logging as log

service_up=Popen("python Service 50001",stdout=PIPE,stdin=None,close_fds=True, shell=True, )
print service_up
time.sleep(100)
