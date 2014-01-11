import logging

MOD_SETTING_MSG = "message"
SET_TEXT_END = "TEXT_END"

__setting = {}
import setting
def set(settingDict):
    logging.debug("Init setting:\n%s" % settingDict.__str__())

    setting.__setting = settingDict

def read(moudel):
    logging.debug("Read %s of setting:\n%s" %( moudel,__setting))

    return setting.__setting[moudel]
