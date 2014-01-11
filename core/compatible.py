"""The moudel for compatible to sae"""
import settings


def getmc():
    severSet = settings.read(settings.MOD_SETTING_SERVER)
    if severSet[settings.SET_SERVER_ONSAE]:
        import pylibmc
        mc = pylibmc.Client()
        return mc
    else:
        import memcache
        mc = memcache.Client([severSet[settings.SET_SERVER_MEMCACHE]])
        return mc
