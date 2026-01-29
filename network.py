# -*- coding: utf-8 -*-
import os, time
from .paths import TMP_BISS, BISS_TXT_URL
from .config import config

try:
    from urllib.request import urlopen, urlretrieve
except ImportError:
    from urllib2 import urlopen
    from urllib import urlretrieve

def get_biss_data():
    cache_time = int(config.plugins.bisspro.cache_time.value)
    if cache_time > 0 and os.path.exists(TMP_BISS):
        if time.time() - os.path.getmtime(TMP_BISS) < cache_time * 60:
            return open(TMP_BISS, "r").read().upper()
    data = urlopen(BISS_TXT_URL, timeout=10).read()
    if isinstance(data, bytes):
        data = data.decode("utf-8", "ignore")
    open(TMP_BISS, "w").write(data.upper())
    return data.upper()
