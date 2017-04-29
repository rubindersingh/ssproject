import os
import re
import sys
from xml.dom.minidom import parse
import xml.dom.minidom
DOMTree = xml.dom.minidom.parse("config.xml")

class format_string:
	def filterOut(self, port, args_list_user):
		count=0		
		pattern_list=[]
		configuration = DOMTree.documentElement
		services = configuration.getElementsByTagName("service")
		for service in services:
			if service.getAttribute('port') == port :
				filters= service.getElementsByTagName("filters")
				for filt in filters:
					fil=filt.getElementsByTagName("filter")
					for f in fil:
						if f.getAttribute("name")=="format_string":
							lists=f.getElementsByTagName("pattern")
							for l in lists:
								count=count+1	
							for i in range(0,count):
								lists=f.getElementsByTagName("pattern")[i]
								pattern=lists.childNodes[0].data
								pattern_list.append(pattern)
			for args in args_list_user:
				for pat in pattern_list:
					a = str(args)
					check = re.search(pat, a)		
					if check is not None:
						print("\n*************************ERROR****************\n")
						return False
			print("SUCCESS FORMAT ")
			return True
