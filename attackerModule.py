import sys


varList=[]
varDict={}


def attackService(args):
    print "Inside service"
    print args



#****** Instructions for attack command input ********
#all var must start with $ (other than service var)
#if var starts with _ then its a service var else global var
#sample command "30*$nop $shellcode 40*$nop $address"
attackCommand = raw_input("Enter the attack command: ")

commandList = attackCommand.split(" ")
print commandList

for i in range(len(commandList)):
    indexVar = commandList[i].find("$")
    if(indexVar>=0 and commandList[i][indexVar:] not in varList):
        varList.append(commandList[i][indexVar:])
        
if(varList):
    varDict={}
    print varList
    
    for i in range(len(varList)):
        varDict[varList[i]]=raw_input(varList[i]+" : ")
        
        
    print varDict
    
print commandList

for i in range(len(commandList)):
    indexVar = commandList[i].find("$")
    if(indexVar>=0 and varDict[commandList[i][indexVar:]]):
            commandList[i]=commandList[i][:indexVar]+varDict[commandList[i][indexVar:]]
        
print commandList


attackService(commandList)
