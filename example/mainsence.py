from core.sences import *
from core.scopes import *

class MainSence(Sence):
    def _onShow(self,input,scope):
        scope["hi"] = ["hello1","hehe2"]
        scope["hehe"] = {"ha":"haha"}
        return self.showView("newsview",scope)

    def _onInput(self,input,scope):
        if input.getContent() == "textmod":
            changeTextMode(scope)
            scope["textmod"] = getTextMode(scope)
            return self.showView("textmod_view",scope)
        
            
        return self._onShow(input,scope)

   
