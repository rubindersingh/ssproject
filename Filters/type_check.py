from xml.dom.minidom import parse
import xml.dom.minidom
import sys
import re

arglist = [88.90, 'apple']
DOMTree = xml.dom.minidom.parse("config.xml")

class type_check:


    def filterOut(self, port, arglist):

        configuration = DOMTree.documentElement
        services = configuration.getElementsByTagName("service")

        for service in services:
            if service.getAttribute("port") == port:
                arguments = service.getElementsByTagName("arg")
                count = 0
                for argument in arguments:
                    if str(argument.getElementsByTagName("position")[0].childNodes[0].data) == str(count):
                        regex_check = re.fullmatch(argument.getElementsByTagName('regex')[0].childNodes[0].data,str(arglist[count]))
                        if not regex_check:
                            print("\n*************************ERROR****************\n")
                        else:
                            print("TYPE SUCCESS")
                    count += 1
                break
