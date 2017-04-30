from xml.dom.minidom import parse
import xml.dom.minidom
import sys
import re
from ast import literal_eval

arglist = [88.90, 'apple']
DOMTree = xml.dom.minidom.parse("config.xml")

class type_check:
    def filterOut(self, service, argList):
        for (pos, name, object) in argList:
            if name is not None:
                arg = service.expected_args[name]
            else:
                arg = service.expected_args[pos]

            if arg.attrib.get('type', None) is not None:
                if get_type(object) is not arg.attrib.get('type'):
                    return False
                else:
                    object = convert(arg.attrib.get('type', None), object)
            if arg.attrib.get('min_value', None) is not None:
                if object < convert(arg.attrib.get('type', arg.attrib.get('min_value'))):
                    return False
            if arg.attrib.get('max_value', None) is not None:
                if object > convert(arg.attrib.get('type', arg.attrib.get('min_value'))):
                    return False
            if arg.attrib.get('min_length', None) is not None:
                if len(str(object)) < int(arg.attrib.get('min_length')):
                    return False
            if arg.attrib.get('max_length', None) is not None:
                if len(str(object)) > int(arg.attrib.get('max_length')):
                    return False
            if arg.attrib.get('length', None) is not None:
                if len(str(object)) != int(arg.attrib.get('length', None)):
                    return False
            if arg.attrib.get('regex', None) is not None:
                pattern = re.compile(arg.attrib.get('regex'))
                if not pattern.match(str(object)):
                    return False



def get_type(input_data):
    try:
        vartype = str(type(literal_eval(input_data)))
        return vartype[7:len(vartype) - 2]
    except (ValueError, SyntaxError):
        return 'str'


def convert(type, object):
    exec('x=type+"("+object+")"')
    return eval(x)
