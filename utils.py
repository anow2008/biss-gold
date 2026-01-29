# -*- coding: utf-8 -*-
import os, shutil, re
from datetime import datetime
from .softcam import BISS_FILE
from .config import config

def create_backup():
    if not config.plugins.bisspro.backup_enable.value:
        return None

    if os.path.exists(BISS_FILE):
        b = BISS_FILE + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy(BISS_FILE, b)
        cleanup_backups()
        return b
    return None

def cleanup_backups():
    keep = config.plugins.bisspro.backup_keep.value
    base = os.path.dirname(BISS_FILE)
    name = os.path.basename(BISS_FILE)
    backups = sorted([f for f in os.listdir(base) if f.startswith(name + ".bak_")])
    while len(backups) > keep:
        old = backups.pop(0)
        try:
            os.remove(os.path.join(base, old))
        except:
            pass

def clean_biss_key(key):
    return re.sub(r'[^0-9A-F]', '', key.upper())

def normalize(text):
    return ''.join(c for c in text.upper() if c.isalnum())
