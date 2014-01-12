"""Moudel of scope
For keep var between code and view(and it will be stronge in memcached by openID)
"""
KEY_SENCE = "_rainkey__sence"

SCOPE_LIFETIME = 300        #The time scope existed in memcached


from compatible import *
import json
import logging

def getSenceName(scope):
    if scope.has_key(KEY_SENCE):
        return scope[KEY_SENCE]
    else:
        return None

def setSenceName(scope,senceName):
    scope[KEY_SENCE] = senceName


class ScopeControl(object):
    def __init__(self,openID,sever):
        self.__mckey = sever + "." + openID
        self.__scope = self.__loadScope()
        logging.debug("scope inited:\n%s" % self.__scope.__str__())


    def getScope(self):
        return self.__scope

    def __loadScope(self):
        logging.debug("Ready to load scope from memcache")
        mc = getmc()
        scopeJSON = mc.get(self.__mckey)
        scope = {}

        if scopeJSON is not None :
            scope = json.loads(scopeJSON)
        else:
            pass

        return scope

    def update(self):
        mc = getmc()
        scopeJSON = json.dumps(self.__scope)
        mc.set(self.__mckey,scopeJSON,SCOPE_LIFETIME)
        logging.debug("scope update:\n%s" % scopeJSON)


