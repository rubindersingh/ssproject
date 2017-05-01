import re
import ast
import sys

class type_check:
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
                    print "Type Check - config: Arg with Name: %s, POS: %s, Value: %s is invalid" % (name, pos, object)
                    return False

                # Check type and verify
                casted_object = None
                if arg.attrib.get('type', None) is not None:
                    if arg.attrib.get('type') != "str":
                        casted_object = self.evalObject(object)
                    else:
                        casted_object = object

                    if self.get_type(casted_object) != arg.attrib.get('type'):
                        print "Type Check - type: Arg with Name: %s, POS: %s, Value: %s is invalid" % (
                            name, pos, object)
                        return False

                # If min_value attr is present
                if arg.attrib.get('min_value', None) is not None:
                    if casted_object < self.evalObject(arg.attrib.get('min_value')):
                        print "Type Check - min_value: Arg with Name: %s, POS: %s, Value: %s is invalid" % (
                            name, pos, object)
                        return False

                # If max_value attr is present
                if arg.attrib.get('max_value', None) is not None:
                    if casted_object > self.evalObject(arg.attrib.get('max_value')):
                        print "Type Check - max_value: Arg with Name: %s, POS: %s, Value: %s is invalid" % (
                            name, pos, object)
                        return False

                # If min_length attr is present
                if arg.attrib.get('min_len', None) is not None:
                    if len(casted_object) < int(arg.attrib.get('min_len')):
                        print "Type Check - min_length: Arg with Name: %s, POS: %s, Value: %s is invalid" % (
                            name, pos, object)
                        return False

                # If max_length attr is present
                if arg.attrib.get('max_len', None) is not None:
                    if len(casted_object) > int(arg.attrib.get('max_len')):
                        print "Type Check - max_length: Arg with Name: %s, POS: %s, Value: %s is invalid" % (
                            name, pos, object)
                        return False

                # If max_length attr is present
                if arg.attrib.get('len', None) is not None:
                    if len(casted_object) != int(arg.attrib.get('len')):
                        print "Type Check - length: Arg with Name: %s, POS: %s, Value: %s is invalid" % (
                            name, pos, object)
                        return False

                # If regex attr is present
                if arg.attrib.get('regex', None) is not None:
                    pattern = re.compile(arg.attrib.get('regex'))
                    if not pattern.match(object):
                        print "Type Check - regex: Arg with Name: %s, POS: %s, Value: %s is invalid" % (
                            name, pos, object)
                        return False
        except Exception, err:
            print 'type_check - ERROR: %sn' % str(err)
            return True




