import os
import re
import sys
from xml.dom.minidom import parse
import xml.dom.minidom

DOMTree = xml.dom.minidom.parse("config.xml")


class num_of_args:
    def filterOut(self, service, argList):
        data_count = len(argList)

        arg_count = 0
        req_count = 0
        for (pos, name, object) in argList:
            if service.expected_args[name] is not None:
                arg_count += 1
                if service.required_args[name] is not None:
                    req_count += 1

        if data_count < req_count:
            return False
        return True
