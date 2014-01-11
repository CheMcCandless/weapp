#-*- coding: utf-8 -*-

"""Main moudel of weapp"""

from core.message import *
from core import setting

class Weapp(object):

    def __init__(self,settingDict):
        logging.debug("Init weapp")
        setting.set(settingDict)


    def run(self,postData):
        logging.debug("Run weapp with post data:\n%s" % postData)
        msg = load_msg(postData)
        return msg.getForPut("test","test")
