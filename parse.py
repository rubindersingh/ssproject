def delimiter(argString, outer, inner):

    argValues = {}
    arglist = argString.split(outer)
    if inner:
        position = 0
        for arg in arglist:
            if inner in arg:
                key, value = arg.split(inner)
                argValues[key] = value
                position += 1
            else:
                argValues[position] = arg
                position += 1
        return argValues
    else:
        position = 0
        for arg in arglist:
            argValues[position] = arg
            position += 1
        return argValues

# print(delimiter("a:2 b:3 c:4", " ", ":"))
# print(delimiter("q='qwe'&w='asd'&e='zxc'", "&", "="))
# print(delimiter("a b c", " ", ""))
# print(delimiter("a='123123' b c=3", " ", "="))

# def delim(input, outer, inner):
#     index = 0
#     argValues = []
#     for pattern in inner:
#         a = input.find(pattern)
#         b = input.find(outer)
#         argValues.append(input[a + len(pattern):b])
#         input = input[b + 1:]
#     return argValues
#
# input = "MynameisAppleMypasswordisBob Provide Flag for Cat"
# print(delim(input, ";", ["is ", "is ", "for "]))
#
# # inputo = "<data><name>Apple</name><password>Ball<password><FlagID>Cat</FlagID></data>"
# # print(delim(input, ";", ["is ", "is ", "for "]))

def delim(input, pattern):
    from difflib import ndiff
    input = input + "$"             # CONVENIENCE
    pattern = pattern + "$"         # CONVENIENCE
    diff = ndiff(input, pattern)
    diff = list(diff)
    res = []
    argValues = []
    for dif in diff:
        if "-" in dif:
            ch = dif[-1:]
            res.append(ch)
            if "-" not in diff[(diff.index(dif)) + 1]:
                res.append(" ")
            pass
    values = ''.join(res[:-1])
    argValues = values.split(' ')
    #print(argValues)
    return argValues


pattern = "My name is .\nMy password is .\nProvide Flag for ."
input = "My name is Apple.\nMy password is Bob.\nProvide Flag for Cat."
print(delim(input, pattern))

pattern1 = "<data><name></name><paswsword></password><FlagID></FLAGID></data>"
input1 = "<data><name>ABC</name><paswsword>DEF</password><FlagID>GHI</FLAGID></data>"
print(delim(input1, pattern1))