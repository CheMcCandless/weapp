"""The moudel for compatible to sae"""
onsae = false

def getmc():
    import memcache
    mc = memcache.Client(['127.0.0.1:12333'])
    return mc
