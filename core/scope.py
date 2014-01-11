"""Moudel of scope
For keep var between code and view(and it will be stronge in memcached by openID)
"""
class ScopeControl(object):
    def __init(self,openID):
        self.__scope = {}

    def getScope(self):
        return self.__scope


