import os
import re
import sys
from xml.dom.minidom import parse
import xml.dom.minidom

DOMTree = xml.dom.minidom.parse("config.xml")


class num_of_args:
    def filterOut(self, port, arglist):
        count = 0
        args_num = len(arglist)

        configuration = DOMTree.documentElement
        services = configuration.getElementsByTagName("service")
        for service in services:
            if service.getAttribute('port') == str(port):
                arguments = service.getElementsByTagName("expected_args")
                for args in arguments:
                    arg = args.getElementsByTagName('arg')
                    for a in arg:
                        count = count + 1

                if args_num != count:
                    print("\n**********ERROR*****************\n")
                    return False
                print("SUCCESS NUM_OF_ARGS")
                return True

            # if args_num != count:
            # 	print("\n*************************ERROR****************\n")
            # return False
            # print("SUCCESS")
            # return True
