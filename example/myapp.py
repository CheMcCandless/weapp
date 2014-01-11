import sys
sys.path.append("..")

from main import *
from mainsence import *

class MyApp(WeApp):
    def _onInit(self):
        self.setMainSence(MainSence)
        self.newSence("MainSence",MainSence)
