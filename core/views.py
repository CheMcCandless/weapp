import logging
import json

from litetemplate import *
from messages import *

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
        logging.debug("Scope after initrepeat:\n%s" % scope)
        self.__syncScope(viewcode,scope)
        logging.debug("Scope after sync:\n%s" % scope)
        self.__message = NewsMessage(viewcode[VIEW_ITEMS])


    def __initRepeat(self,viewcode,scope):
        items = viewcode.get(VIEW_ITEMS)
        newitems = []
        for each in items:
          self.__spreadRepeat(viewcode,each,newitems,scope)
    
        viewcode[VIEW_ITEMS] = newitems

    def __spreadRepeat(self,viewcode,item,newitems,scope):
        repate = item.get(VIEW_REPEAT,None)
        if repate is not None:
            lst = repate.split()
            one = lst[0]
            array = lst[2]
            eachjson = json.dumps(item)
            
            for i in range(len(scope[array])):
                newitem_json = eachjson.replace("${"+one,"${"+array+"["+str(i)+"]")
                newitems.append(json.loads(newitem_json))
        else:
            newitems.append(item)
    
    def __syncScope(self,viewcode,scope):
        logging.debug("Scope before sync:\n%s" % scope)
        logging.debug("View before sync:\n%s" % viewcode)
        items = viewcode[VIEW_ITEMS]
        items_json = json.dumps(items)
        t = LiteTemplate(items_json)
        result_json = t.substitute(scope)
        logging.debug("result_json after substitute:\n%s" % result_json)
        viewcode[VIEW_ITEMS] =  json.loads(result_json)

    def getMessage(self):
        return self.__message

