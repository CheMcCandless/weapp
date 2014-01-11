"""The moudel for compatible to sae"""
import settings


def getmc():
    severSet = settings.read(settings.MOD_SETTING_SEVER)
    if severSet[settings.SET_SEVER_ONSAE]:
        import pylibmc
        mc = pylibmc.Client()
        return mc
    else:
        import memcache
        mc = memcache.Client([severSet[settings.SET_SEVER_MEMCACHE]])
        return mc
