from core.sences import *

class MainSence(Sence):
    def _onShow(self,input,scope):
        scope["hi"] = "hello"
        return self.showView("mainview",scope)

    def _onInput(self,input,scope):
        return self._onShow(input,scope)

    def __init__(self):
        self._R = {
            "mainview":{
                "type":"text",
                "content":"This is just a test $hi"
            }
        }
