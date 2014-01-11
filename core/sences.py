from scopes import *
class Sence(object):
    def __init__(self):
        pass


    def show(self,message,scope):
        logging.debug("Show sence %s" % self.__class__.__name__)
        setSenceName(scope,self.__class__.__name__)
        return self._onShow(scope)

    def _onShow(self,message,scope):
        pass

    def _onInput(self,message,scope):
        pass

class SenceControl(object):
    def __init__(self):
        self.__senceList = {}
        self.__mainSence = None

    def newSence(self,senceName,senceType):
        self.__senceList[senceName] = senceType

    def setMainSence(self,senceType):
        self.__mainSence = senceType

    def run(self,message,scope):
        senceName = getSenceName(scope)
        if senceName is not None:
            sence = self.__senceList[senceName]()
        else:
            sence = self.__mainSence()
        sence._onInput(message,scope)



