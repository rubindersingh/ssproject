import xml.etree.ElementTree as ET
import os
import sys

class Configuration:

    def __init__(self, fileName, reload=-1):
        tree = ET.parse(fileName)
        self.fileName = fileName
        self.lastchanged = os.stat(fileName).st_mtime
        self.configuration = tree.getroot()
        self.services = {}
        for service in self.configuration.find("services"):
            self.services[int(service.find("external_port").text)] = Service(service)

    def getService(self, port):
        return self.services[port]

    def reloadService(self, port):
        modTime = os.stat(self.fileName).st_mtime
        if modTime != self.lastchanged:
            tree = ET.parse(self.fileName)
            self.lastchanged = modTime
            self.configuration = tree.getroot()
            self.services = {}
            for service in self.configuration.find("services"):
                self.services[int(service.find("external_port").text)] = Service(service)
        return self.services[port]

class Service:
    def __init__(self, service):
        self.internal_port = int(service.find("internal_port").text)
        self.external_port = int(service.find("external_port").text)
        self.start_cmd = service.find("start_cmd").text
        self.stop_cmd = service.find("stop_cmd").text
        self.buffer = int(service.find("buffer").text)
        self.max_payload = int(service.find("max_payload").text)
        self.req_queue_size = int(service.find("req_queue_size").text)
        self.pos_expected_args = {}
        self.named_expected_args = {}
        args = service.find("expected_args")
        self.max_args = 0
        self.min_args = 0
        self.required_args = {}
        self.optional_args = {}

        for arg in args:
            self.max_args += 1
            if arg.attrib.get('required', 0) == "1":
                self.min_args += 1
                if arg.attrib.get('name', None) is not None:
                    if not self.named_expected_args.has_key(arg.attrib['name']):
                        self.named_expected_args[arg.attrib['name']] = arg
                        self.required_args[arg.attrib['name']] = arg
                    else:
                        print "Duplicate name argument"
                        exit(0)
                elif arg.attrib.get('position', None) is None:
                    print "Position is required if name not given"
                    exit(0)

                if arg.attrib.get('position', None) is not None:
                    if not self.pos_expected_args.has_key(int(arg.attrib['position'])):
                        self.pos_expected_args[int(arg.attrib['position'])] = arg
                        self.required_args[int(arg.attrib['position'])] = arg
                    else:
                        print "Duplicate position argument"
                        exit(0)
            else:
                if arg.attrib.get('name', None) is not None:
                    if not self.named_expected_args.has_key(arg.attrib['name']):
                        self.named_expected_args[arg.attrib['name']] = arg
                        self.optional_args[arg.attrib['name']] = arg
                    else:
                        print "Duplicate name argument"
                        exit(0)
                elif arg.attrib.get('position', None) is None:
                    print "Position is required if name not given"
                    exit(0)

                if arg.attrib.get('position', None) is not None:
                    if not self.pos_expected_args.has_key(int(arg.attrib['position'])):
                        self.pos_expected_args[int(arg.attrib['position'])] = arg
                        self.optional_args[int(arg.attrib['position'])] = arg
                    else:
                        print "Duplicate position argument"
                        exit(0)

        self.parser=service.find("parser")
        filterXML = service.find("filters")
        self.filters = {}
        self.filterList = []
        for filter in filterXML:
            self.filterList.append(filter)


