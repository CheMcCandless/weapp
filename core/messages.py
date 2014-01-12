#-*- coding: utf-8 -*-
"""Moudel of message classes"""


import time
import xml.etree.ElementTree as ET
from abc import ABCMeta, abstractmethod
from string import Template
import logging
import json

import settings

VIEW_TYPE = "type"
VIEW_TEXT = "content"
VIEW_TYPE_TEXT = "text"

VIEW_TYPE_NEWS = "news"
VIEW_TYPE_ITEMS = "items"
VIEW_NEWS_TITLE = "title"
VIEW_NEWS_DESCRIPTION = "description"
VIEW_NEWS_PICURL = "picurl"
VIEW_NEWS_URL = "url"


def loadview(viewcode, scope):
    logging.debug("Begin to load view:\n%s" % viewcode)

    viewjson = json.dumps(viewcode)
    t = Template(viewjson)
    viewjson = t.safe_substitute(scope)
    viewcode = json.loads(viewjson)

    viewdict = {
        VIEW_TYPE_TEXT: loadview_text,
        VIEW_TYPE_NEWS: loadview_news
    }
    return viewdict[viewcode[VIEW_TYPE]](viewcode)


def loadview_text(viewcode):
    '''
    {
        "type" : "text",
        "content" : "content"
    }
    '''
    return TextMessage(viewcode[VIEW_TEXT])


def loadview_news(viewcode):
    '''
    {
        "type" : "news",
        "items" : [
            {
                "title" : title,
                "description" : description,
                "picurl" : picurl
                "url" : url
            },
            ...
        ]
    }
    '''
    items = viewcode[VIEW_TYPE_ITEMS]
    return NewsMessage(items)


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

    def __init__(self, *items):
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
        for i in items[0]:
            logging.debug(i)
            onexml = itemxml % (i[VIEW_NEWS_TITLE],i[VIEW_NEWS_DESCRIPTION],i[VIEW_NEWS_PICURL],i[VIEW_NEWS_URL])
            itemsxml.append(onexml)

        articlesxml = "".join(itemsxml)
        self._xml = self._xml % (len(items[0]), articlesxml)
