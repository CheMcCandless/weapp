#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
'''
微信Server模拟
'''
import requests

messages = {
    # 用户关注消息
    'text': '''<xml>
    <ToUserName><![CDATA[falling_server]]></ToUserName>
    <FromUserName><![CDATA[falling]]></FromUserName>
    <CreateTime>1348831860</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    <MsgId>1234567890123456</MsgId>
    </xml>'''
}


def makePost(url, type, content):
    xml = messages[type] % content
    r = requests.post(url, xml)
    print(r.text)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("The right cmd is just like:python wei.py http://127.0.0.1/ text test")
    else:
        makePost(sys.argv[1], sys.argv[2], sys.argv[3])
