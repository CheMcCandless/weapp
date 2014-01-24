""" Different from string.Template,
    - LiteTemplate will eval every value
    - LiteTemplate uesd ${var} instaed of $var
"""
import re
import logging
import copy

class LiteTemplate(object):
    def __init__(self,tlpstring):
        self.__tlpstring = tlpstring
        
    def substitute(self,match):
        r = re.compile("[$]{.*?}")
        consts = r.split(self.__tlpstring)
        vars = r.findall(self.__tlpstring)
        if vars == []:
            return self.__tlpstring
        else:
            values = []
            for var in vars:
                var = var[2:-1]
                matchCache = copy.deepcopy(match)
                values.append(str(eval(var,matchCache)))
            values.append('')
            
            result = ''
            for i in range(len(consts)):
                result = result + (consts[i] + values[i])
            logging.debug("String after substitute:\n%s" % result)
            return result

