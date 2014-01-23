from core.sences import *

class MainSence(Sence):
    def _onShow(self,input,scope):
        scope["hi"] = ["hello1","hehe2"]
        return self.showView("newsview",scope)

    def _onInput(self,input,scope):
        return self._onShow(input,scope)

    def __init__(self):
        self._R = {
            "mainview":{
                "type":"text",
                "content":"This is just a test $hi"
            },
            "newsview":{
                "items":[
                    {
                        "title" : "Test$one",
                        "description" : "None",
                        "picurl":"pic",
                        "url":"www.baidu.com",
                        "repeat":"one in hi"
                    },
                    {
                        "title" : "Test222$hi",
                        "description" : "None",
                        "picurl":"pic",
                        "url":"www.baidu.com"
                    },
                ]
            }
        }
