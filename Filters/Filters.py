from xml.dom.minidom import parse
import xml.dom.minidom
import os
from importlib import import_module
import sys




args_list_user = []
port = 5000




sys.path.append('C:\\Users\\addy3\PycharmProjects\dump')
DOMTree = xml.dom.minidom.parse("config.xml")

configuration = DOMTree.documentElement

services = configuration.getElementsByTagName("service")

def my_import(name):
   components = name.split('.')
   mod = __import__(components[0])
   for comp in components[1:]:
       mod = getattr(mod, comp)
   return mod

for service in services:
    print("\n********SERVICE********")
    if service.hasAttribute("port"):
        print("PORT NUMBER: " + service.getAttribute("port"))
        print("PUBLIC PORT: " + service.getElementsByTagName('pub')[0].childNodes[0].data)

    filters = service.getElementsByTagName("filter")

    for filter in filters:
        if filter.hasAttribute("name"):
            #print("DISPATCHED TO FILTER: " + filter.getAttribute("name") + "\t\t\tWith Service Port: " + service.getAttribute("port"))

            filter_name = str(filter.getAttribute('name')) + "." + str(filter.getAttribute('name'))
            #print(filter_name)

            import_filter = my_import(str(filter_name))

            obj = import_filter()
            obj.filterOut(port, args_list_user)
            #os.system("python " + filter.getAttribute("name") + ".py " + service.getAttribute("port"))
            #os.system("python num_of_args.py 5000")

            # if filter.getElementsByTagName('next'):
            #     print("Next Filter in Chain: " + filter.getElementsByTagName("next")[0].childNodes[0].data)

#os.system("python type_check.py 6000")