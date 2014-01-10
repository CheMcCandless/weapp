#-*- coding: utf-8 -*-

"""Main moudel of weapp"""

from core.message import *

class Weapp(object):
    def __init__(self,setting):
        logging.debug("Init weapp with setting\n%s" % setting.__str__())
        self.__setting = setting
        pass

    def run(self,postData):
        logging.debug("Run weapp with post data:\n%s" % postData)
        msg = load_msg(postData)
        return msg.getForPut("test","test")
