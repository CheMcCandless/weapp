import logging

MOD_SETTING_MSG = "message"
SET_TEXT_END = "textend"

MOD_SETTING_SEVER = "sever"
SET_SEVER_ONSAE = "onsae"
SET_SEVER_MEMCACHE = "mem"

__setting = {}
import settings
def set(settingDict):
    logging.debug("Init setting:\n%s" % settingDict.__str__())

    settings.__setting = settingDict

def read(moudel):
    logging.debug("Read %s of setting:\n%s" %( moudel,__setting))

    return settings.__setting[moudel]
