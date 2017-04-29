import os
import re
import sys
from xml.dom.minidom import parse
import xml.dom.minidom
DOMTree = xml.dom.minidom.parse("config.xml")

class buffer_overflow:
	def filterOut(self, port, args_list_user):
		count=0
		pattern_list=[]
		configuration = DOMTree.documentElement
		services = configuration.getElementsByTagName("service")
		for service in services:
			if service.getAttribute('port') == port:
				filters= service.getElementsByTagName("filter")
				for f in filters:
					if f.getAttribute("name")=="buffer_overflow":
						lists=f.getElementsByTagName("pattern")
						for l in lists:
							count=count+1	
						for i in range(0,count):
							lists=f.getElementsByTagName("pattern")[i]
							pattern=lists.childNodes[0].data
							pattern_list.append(pattern)
						#break
				#break
		for args in args_list_user:
			for pat in pattern_list:
				print(str(pat))
				a = str(args)
				check = re.search(pat, a)		
				if check is not None:
					print("\n*************************ERROR****************\n")
					return False
		print("SUCCESS BUFFER OVERFLOW ")
		return True



	







	


