#-*- coding: utf-8 -*-

from bottle import *
import logging

import sys
sys.path.append("..")

from main import Weapp

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[func:%(funcName)s][line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')

debug(True)


@route('/')
def index():
    app = Weapp()
    return app.run()

run(host='localhost', port=8080)