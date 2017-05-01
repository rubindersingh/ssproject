import re
import string

def extractVariables(input, pattern):
    regex = re.sub(r'{\$(.+?);}', r'(?P<_\1>.+)', pattern)
    values = list(re.search(regex, input).groups())
    keys = re.findall(r'{(.+?)}', pattern)
    pairs = dict(zip(keys, values))
    return pairs

def extractArgList(data):
    pattern='hello, my name is {$name;} and I am a {$age;} year old {$what;}'
    pairs = extractVariables(data, pattern)
    #print pairs

    argList=[]
    for k,v in pairs.iteritems():
        pos = len(argList)
        name=str(k.split('$')[1].split(';')[0])
        value=v
        argList.append((pos,str(name),value))

    return argList

#p = 'hello, my name is {$name;} and I am a {$age;} year old {$what;}'
#t = 'hello, my name is Rubinder and I am a 27 year old [1,2,3,4,5]'

#extractArgList(t, p)