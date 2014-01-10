#-*- coding: utf-8 -*-
"""Moudel of message classes"""

SET_TEXT_END = "TEXT_END"

import time
import xml.etree.ElementTree as ET
from abc import ABCMeta, abstractmethod
from string import Template
import logging


def __parse_msg(xml):
    # To parse the xml message receive from user post

    logging.debug("Begin to parse message xml")

    root = ET.fromstring(xml)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    logging.debug("Success to parse" + "\n" + msg.__str__())
    return msg

def __load_text_msg(info,msgSetting):
    logging.debug("Begin to load text message")
    return TextMessage (info["Content"],msgSetting)




# Load from xml existed
def load_msg(xml,msgSetting):
    """ Load message from xml.

    @param [string] xml
    @return [Message] message
    """
    logging.debug("Begin to load message from xml %s" % xml)

    info = __parse_msg(xml)

    msg_dict = {
        "text" : __load_text_msg
    }

    if msg_dict.has_key(info["MsgType"]):
        logging.debug("Message type:%s" % info["MsgType"])
        return msg_dict [info["MsgType"]](info,msgSetting)
    else:
        logging.debug("None message type[%s]" % info["MsgType"])





class Message(object):
    __metaclass__ = ABCMeta
    def __init__(self):
        self._xml = ''          # XML string for the message


    def getForPut(self,fromUserName,toUserName):
        logging.debug("Ready to put XML:\n%s" % self._xml)
        return self._xml


class TextMessage(Message):
    def __init__(self,content,msgSetting):
        logging.debug("Init textmessage[%s]" % content)

        if   msgSetting.has_key(SET_TEXT_END):
            content = content + msgSetting[SET_TEXT_END]

        xmlTlp = '''<xml>
        <ToUserName><![CDATA[$ToUserName]]></ToUserName>
        <FromUserName><![CDATA[$FromUserName]]></FromUserName>
        <CreateTime>$CreateTime</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[$Content]]></Content>
        <FuncFlag>0</FuncFlag>
        </xml>'''

        s = Template(xmlTlp)
        self._xml = s.safe_substitute({"Content":content})
