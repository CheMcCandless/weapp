#-*- coding: utf-8 -*-

from bottle import *
import logging

import sys
sys.path.append("..")

from myapp import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[func:%(funcName)s][line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')

debug(True)

setting = {
    "message":{
            "textend" : "Powered by JNRain R&C"
    },
    "sever":{
            "onsae" : False,
            "mem" : "127.0.0.1:12000"
    }

}

@post('/')
def index():
    app = MyApp(setting)
    return app.run(request.body.read())

run(host='localhost', port=8080)
