from inspect import getframeinfo, stack
import resource


def print_memory(message = "Max Memory"):
    caller = getframeinfo(stack()[1][0])
    usageinfo = resource.getrusage(resource.RUSAGE_SELF)
    
    print("{}/{} | {}: {:.2f}MB".format(caller.filename, caller.lineno, message, usageinfo.ru_maxrss/1024))


def csv_memory(message = "Memory"):
    caller = getframeinfo(stack()[1][0])
    usageinfo = resource.getrusage(resource.RUSAGE_SELF)
    
    return('"{}","{}",{:.4f}'.format(caller.filename, message, usageinfo.ru_maxrss/1024))