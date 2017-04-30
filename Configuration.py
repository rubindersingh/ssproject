import xml.etree.ElementTree as ET

from __builtin__ import file
from twisted.application.strports import service

from pip._vendor.html5lib import filters


class Configuration:

    def __init__(self, fileName, reload=-1):
        tree = ET.parse(fileName)
        self.configuration = tree.getroot()
        self.services = {}
        for service in self.configuration.find("services"):
            self.services[int(service.find("external_port").text)] = Service(service)

    def getService(self, port):
        return self.services[port]

class Service:
    def __init__(self, service):
        self.internal_port = int(service.find("internal_port").text)
        self.external_port = int(service.find("external_port").text)
        self.start_cmd = service.find("start_cmd").text
        self.expected_args = {}
        args = service.find("expected_args")
        self.max_args = 0
        self.min_args = 0
        self.required_args = {}
        self.optional_args = {}
        i = 0
        for arg in args:
            self.max_args += 1
            if arg.attrib.get('required', 0) == "1":
                self.min_args += 1
                if arg.attrib.get('name', None) is not None:
                    self.expected_args[arg.attrib['name']] = arg
                    self.required_args[arg.attrib['name']] = arg
                elif arg.attrib.get('position', None) is not None:
                    self.expected_args[int(arg.attrib['position'])] = arg
                    self.required_args[int(arg.attrib['position'])] = arg
                else:
                    self.expected_args[i] = arg
                    self.required_args[i] = arg
            else:
                if arg.attrib.get('name', None) is not None:
                    self.expected_args[arg.attrib['name']] = arg
                    self.optional_args[arg.attrib['name']] = arg
                elif arg.attrib.get('position', None) is not None:
                    self.expected_args[int(arg.attrib['position'])] = arg
                    self.optional_args[int(arg.attrib['position'])] = arg
                else:
                    self.expected_args[i] = arg
                    self.optional_args[i] = arg
            i = i+1

        filterXML = service.find("filters")
        self.filters = {}
        self.filterList = []
        for filter in filterXML:
            self.filterList.append(filter)


