import logging
import json
from string import Template

from messages import NewsMessage

VIEW_ITEMS = "items"
VIEW_TITLE = "title"
VIEW_DESCRIPTION = "description"
VIEW_URL = "url"
VIEW_PICURL = "picurl"
VIEW_REPEAT = "repeat"
VIEW_TAG = "tag"

class View:
    def __init__(self,viewcode,scope):
        """Init View from a dict just like:
        {
            "items" : [
                {
                    "title" : "title",
                    "description" : "description",
                    "url" : "url",
                    "picurl" : "url of pictrue",
                    "repeat" : "one in array"
                },...
            ],
            "tags":[]
        }
        """
        self.__initRepeat(viewcode,scope)
        self.__syncScope(viewcode,scope)
        self.__message = NewsMessage(viewcode[VIEW_ITEMS])


    def __initRepeat(self,viewcode,scope):
        items = viewcode.get(VIEW_ITEMS)
        newitems = []
        for each in items:
          self.__spreadRepeat(viewcode,each,newitems,scope)
        viewcode[VIEW_ITEMS] = newitems

    def __makeOneName(self,array,i):
        return "__array_" + array + i.__str__()

    def __flatArray(self,array,scope):
        for i in range(len(scope[array])):
            scope[self.__makeOneName(array,i)] =  scope[array][i]

    def __spreadRepeat(self,viewcode,item,newitems,scope):
        repate = item.get(VIEW_REPEAT,None)
        if repate is not None:
            lst = repate.split()
            one = lst[0]
            array = lst[2]
            self.__flatArray(array,scope)
            eachjson = json.dumps(item)
            t = Template(eachjson)
            
            for i in range(len(scope[array])):
                newitem_json = t.safe_substitute({one:"$"+self.__makeOneName(array,i)})
                newitems.append(json.loads(newitem_json))
        else:
            newitems.append(item)
    
    def __syncScope(self,viewcode,scope):
        logging.debug("Scope before sync:\n%s" % scope)
        items = viewcode[VIEW_ITEMS]
        items_json = json.dumps(items)
        t = Template(items_json)
        result_json = t.safe_substitute(scope)
        viewcode[VIEW_ITEMS] =  json.loads(result_json)

    def getMessage(self):
        return self.__message

