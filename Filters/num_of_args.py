class num_of_args:
    def filterOut(self, service, argList):
        given_arg_count = len(argList)
        try:
            if not (given_arg_count <= service.max_args and given_arg_count>=service.min_args):
                return False

            valid_arg_count = 0
            req_arg_count = 0
            for (pos, name, object) in argList:
                arg = None
                req_arg = None
                if name is not None:
                    arg = service.named_expected_args.get(name, None)
                    req_arg = service.required_args.get(name, None)
                else:
                    arg = service.pos_expected_args.get(pos, None)
                    req_arg = service.required_args.get(pos, None)

                if arg is not None:
                    valid_arg_count += 1
                    if req_arg is not None:
                        req_arg_count += 1
                else:
                    print "Arg with Name: %s, POS: %s, Value: %s is invalid" % (name, pos, object)
                    return False

            if req_arg_count!=service.min_args:
                return False
        except Exception, err:
            print 'num_of_args - ERROR: %sn' % str(err)
        return True