"""The moudel for compatible to sae"""
import setting


def getmc():
    severSet = setting.read(setting.MOD_SETTING_SEVER)
    if severSet[setting.SET_SEVER_ONSAE]:
        pass
    else:
        import memcache
        mc = memcache.Client(severSet[setting.SET_SEVER_MEMCACHE])
        return mc
