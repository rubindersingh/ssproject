import re
import string

def extractVariables(input, pattern):
    regex = re.sub(r'{\$(.+?);}', r'(?P<_\1>.+)', pattern)
    values = list(re.search(regex, input).groups())
    keys = re.findall(r'{(.+?)}', pattern)
    pairs = dict(zip(keys, values))
    return pairs


p = 'hello, my name is {$name;} and I am a {$age;} year old {$what;}'
t = 'hello, my name is Rubinder and I am a 27 year old [1,2,3,4,5]'

print extractVariables(t, p)
print "hello"

