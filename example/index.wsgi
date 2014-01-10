#-*- coding: utf-8 -*-

from bottle import *
import logging

import sys
sys.path.append("..")

from main import Weapp

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[func:%(funcName)s][line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')

debug(True)

setting = {
    "TEXT_END" : "Powered by JNRain R&C"
}

@post('/')
def index():
    app = Weapp(setting)
    return app.run(request.body.read())

run(host='localhost', port=8080)
