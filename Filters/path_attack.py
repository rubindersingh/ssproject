import os
import re
import sys
from xml.dom.minidom import parse
import xml.dom.minidom
DOMTree = xml.dom.minidom.parse("config.xml")
class path_attack:
	def filterOut(self, port, args_list_user):
		configuration = DOMTree.documentElement
		services = configuration.getElementsByTagName("service")
		for service in services:
			if service.getAttribute('port') == str(port):
				filters= service.getElementsByTagName("filters")
				for filt in filters:
					fil=filt.getElementsByTagName("filter")
					for f in fil:
						if f.getAttribute("name")=="path_attack":
							lists=f.getElementsByTagName("pattern")[0]
							pattern=lists.childNodes[0].data
							#break
				#break
							for args in args_list_user:
								a = str(args)
								check = re.search(pattern, a)
								if check is not None:
									print("\n*************************ERROR****************\n")
									return False
							print(" PATH ATTACK SUCCESS")
							return True

	
				










	


