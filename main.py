#-*- coding: utf-8 -*-

"""Main moudel of weapp"""

from core.messages import *
from core import settings
from core.sences import *
from core.scopes import *

class WeApp(object):

    def __init__(self,settingDict):
        logging.debug("Init weapp")
        settings.set(settingDict)
        self.__control = None

    def run(self,postData):
        logging.debug("Run weapp with post data:\n%s" % postData)
        msg = load_msg(postData)
        self.__control = SenceControl()
        self._onInit()
        scopeCon = ScopeControl(msg.getOpenID(),msg.getServer())
        scope = scopeCon.getScope()

        result = self.__control.run(msg,scope)
        scopeCon.update()

        return result.get(msg.getServer(),msg.getOpenID(),getTextMode(scope))

    def _onInit(self):
        pass

    def newSence(self,senceName,senceType):
        self.__control.newSence(senceName,senceType)

    def setMainSence(self,senceType):
        self.__control.setMainSence(senceType)

