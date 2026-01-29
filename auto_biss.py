# -*- coding: utf-8 -*-
import os
from enigma import iServiceInformation
from .network import get_biss_data
from .utils import clean_biss_key, normalize
from .softcam import BISS_FILE, restartSoftcam
from .config import config
from .lang import _
