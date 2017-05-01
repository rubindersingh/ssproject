import Configuration as conf
import multi_pattern_check
configuration = conf.Configuration("config_test.xml")
service = configuration.getService(50000)
obj = multi_pattern_check.multi_pattern_check()
#print obj.filterOut(service, [(0,None, "27"),(1,None,"27.0"),(2,None, "27"),(3,None, "True"),(4,None, "27"),(5,None, "27"),(6,None, "27"),
#(7, None, "27"), (8,None, "27"), (9,None, "27"), (10,None, "27"), (4,None, "['a', 'b','c']"),(5,None, "{'a':1, 'b':2,'c':3, 4:60.5}"),(6,None, "[1,2,4,4,5]"), ])

print obj.filterOut(service, [(7,None, "27hgfjjhjbjbkjhk  -_@hkh k hkhkjhkjhkjhkjh k jhkj hk hkjhkj hk h")])