# -*- coding: utf-8 -*-
import os, time

def get_key_path():
    paths = [
        "/etc/tuxbox/config/oscam/SoftCam.Key",
        "/etc/tuxbox/config/SoftCam.Key",
        "/usr/keys/SoftCam.Key",
        "/var/keys/SoftCam.Key"
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return "/etc/tuxbox/config/SoftCam.Key"

BISS_FILE = get_key_path()

def restartSoftcam():
    cams = ["oscam", "ncam", "gcam", "revcam", "vicard"]

    from .config import config

    if config.plugins.bisspro.restart_mode.value == "smart":
        active = None
        for c in cams:
            if os.system("pidof %s >/dev/null 2>&1" % c) == 0:
                active = c
                break
        if not active:
            active = "oscam"
        os.system("killall %s 2>/dev/null" % active)
        time.sleep(1)
        path = "/usr/bin/" + active
        os.system("%s -b >/dev/null 2>&1 &" % (path if os.path.exists(path) else active))
    else:
        for c in cams:
            os.system("killall %s 2>/dev/null" % c)
        time.sleep(2)
        cam_to_run = "oscam"
        path = "/usr/bin/" + cam_to_run
        os.system("%s -b >/dev/null 2>&1 &" % (path if os.path.exists(path) else cam_to_run))
