import re
import ast
import sys

class multi_pattern_check:
    def get_type(self, object):
        try:
            vartype = str(type(object))
            return vartype[7:len(vartype) - 2]
        except (ValueError, SyntaxError):
            return 'str'

    def evalObject(self, object):
        try:
            val = ast.literal_eval(object)
            return val
        except (ValueError, SyntaxError):
            return object

    def filterOut(self, service, argList):
        try:
            for (pos, name, object) in argList:
                arg = None
                if name is not None:
                    arg = service.named_expected_args.get(name, None)
                else:
                    arg = service.pos_expected_args.get(pos, None)

                if arg is None:
                    print "multi_pattern_check - config: Arg with Name: %s, POS: %s, Value: %s is invalid" % (name, pos, object)
                    return False

                patterns = arg.findall("pattern")
                if patterns:
                    # Check type and verify
                    casted_object = None
                    if arg.attrib.get('iter', None) == "1":
                        casted_object = self.evalObject(object)
                    else:
                        casted_object = object

                    for pattern in patterns:
                        if pattern.attrib.get("regex", None) is not None:
                            reObj = re.compile(pattern.attrib.get('regex'))
                            if arg.attrib.get('iter', None) == "1":
                                for child in casted_object:
                                    if not reObj.match(str(child)):
                                        print "multi_pattern_check - regex: Arg with Name: %s, POS: %s, Value: %s is invalid for %s" % (
                                            name, pos, child, pattern.attrib.get('regex'))
                                        return False
                            else:
                                if not reObj.match(casted_object):
                                    print "multi_pattern_check - regex: Arg with Name: %s, POS: %s, Value: %s is invalid for %s" % (
                                        name, pos, object, pattern.attrib.get('regex'))
                                    return False

            return True
        except Exception, err:
            print 'multi_pattern_check - ERROR: %sn' % str(err)
            return True




