#-*- coding: utf-8 -*-

"""Main moudel of weapp"""

from core.message import *

class Weapp(object):
    def __init__(self,setting):
        logging.debug("Init weapp with setting\n%s" % setting.__str__())
        self.__setting = setting
        pass

    def run(self):
        logging.debug("Run weapp")
        return TextMessage("textmessage").getForPut("test","test")
