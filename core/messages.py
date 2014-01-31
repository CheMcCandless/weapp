#-*- coding: utf-8 -*-
"""Moudel of message classes"""


import time
import xml.etree.ElementTree as ET
from abc import ABCMeta, abstractmethod
from string import Template
import logging
import json

import settings

VIEW_ITEMS = "items"
VIEW_TITLE = "title"
VIEW_DESCRIPTION = "description"
VIEW_URL = "url"
VIEW_PICURL = "picurl"
VIEW_REPEAT = "repeat"
VIEW_TAG = "tag"


def __parse_msg(xml):
    # To parse the xml message receive from user post

    logging.debug("Begin to parse message xml")

    root = ET.fromstring(xml)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    logging.debug("Success to parse" + "\n" + msg.__str__())
    return msg


def __load_text_msg(info):
    logging.debug("Begin to load text message")
    return TextMessage(info["Content"])


# Load from xml existed
def load_msg(xml):
    """ Load message from xml.

    @param [string] xml
    @return [Message] message
    """
    logging.debug("Begin to load message from xml %s" % xml)

    info = __parse_msg(xml)

    msg_dict = {
        "text": __load_text_msg
    }

    if msg_dict.has_key(info["MsgType"]):
        logging.debug("Message type:%s" % info["MsgType"])

        msg = msg_dict[info["MsgType"]](info)
    else:
        logging.debug("None message type[%s]" % info["MsgType"])

    msg.setOpenID(info["FromUserName"])
    msg.setServer(info["ToUserName"])
    return msg


class Message(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._xml = ''          # XML string for the message
        self.__openID = ''

    def getForPut(self, fromUserName, toUserName):
        logging.debug("Ready to put XML:\n%s" % self._xml)
        t = Template(self._xml)
        xml = t.safe_substitute(
            {"FromUserName": fromUserName, "ToUserName": toUserName, "CreateTime": time.time()})
        return xml

    def setOpenID(self, openID):
        self.__openID = openID

    def getOpenID(self):
        return self.__openID

    def setServer(self, server):
        self.__server = server

    def getServer(self):
        return self.__server


class TextMessage(Message):

    def __init__(self, content):
        self.__content = content
        msgSetting = settings.read(settings.MOD_SETTING_MSG)
        logging.debug("Init textmessage[%s]" % content)

        if msgSetting.has_key(settings.SET_TEXT_END):
            content = content + msgSetting[settings.SET_TEXT_END]

        xmlTlp = '''<xml>
        <ToUserName><![CDATA[$ToUserName]]></ToUserName>
        <FromUserName><![CDATA[$FromUserName]]></FromUserName>
        <CreateTime>$CreateTime</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[$Content]]></Content>
        <FuncFlag>0</FuncFlag>
        </xml>'''

        s = Template(xmlTlp)
        self._xml = s.safe_substitute({"Content": content})

    def getContent(self):
        return self.__content


class NewsMessage(Message):

    def __init__(self, items):
        self.__items = items
        
        logging.debug("Items:" + items.__str__())
        self._xml = '''<xml>
        <ToUserName><![CDATA[$ToUserName]]></ToUserName>
        <FromUserName><![CDATA[$FromUserName]]></FromUserName>
        <CreateTime>$CreateTime</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>%s</ArticleCount>
        <Articles>
            %s
        </Articles>
        </xml>
        '''

        itemxml = '''        <item>
        <Title><![CDATA[%s]]></Title>
        <Description><![CDATA[%s]]></Description>
        <PicUrl><![CDATA[%s]]></PicUrl>
        <Url><![CDATA[%s]]></Url>
        </item>'''

        itemsxml = []
        for i in items:
            logging.debug(i)
            onexml = itemxml % (i[VIEW_TITLE],i.get(VIEW_DESCRIPTION,""),i.get(VIEW_PICURL,""),i.get(VIEW_URL,""))
            itemsxml.append(onexml)


        if settings.read(settings.MOD_SETTING_MSG).has_key(settings.SET_NEWS_END):
            i = settings.read(settings.MOD_SETTING_MSG)[settings.SET_NEWS_END]
            itemsxml.append(itemxml % (i[VIEW_TITLE],i.get(VIEW_DESCRIPTION,""),i.get(VIEW_PICURL,""),i.get(VIEW_URL,"")))

        articlesxml = "".join(itemsxml)
        self._xml = self._xml % (len(itemsxml), articlesxml)

    def get(self,fromUserName, toUserName,bytext = False):
        if bytext:
            text = ""
            for i in self.__items:
                if i.get(VIEW_URL,"") != "":
                    text = text + '<a href="' + i[VIEW_URL] + '">' + i[VIEW_TITLE] +'</a>' + '\n\n'
                else:
                    text = text  + i[VIEW_TITLE] + '\n\n'
            return TextMessage(text).getForPut(fromUserName,toUserName)
        else:
            return self.getForPut(fromUserName,toUserName)