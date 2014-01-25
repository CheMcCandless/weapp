from core.sences import *

class MainSence(Sence):
    def _onShow(self,input,scope):
        scope["hi"] = ["hello1","hehe2"]
        scope["hehe"] = {"ha":"haha"}
        return self.showView("newsview",scope)

    def _onInput(self,input,scope):
        return self._onShow(input,scope)

   
