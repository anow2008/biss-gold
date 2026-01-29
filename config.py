# -*- coding: utf-8 -*-
from Components.config import (
    config, ConfigSubsection,
    ConfigYesNo, ConfigSelection, ConfigInteger
)

config.plugins.bisspro = ConfigSubsection()
config.plugins.bisspro.restart_mode = ConfigSelection(default="smart", choices=[
    ("smart", "Smart Restart (Active CAM only)"),
    ("full", "Full Restart (All CAMs)")
])
config.plugins.bisspro.match_sid = ConfigYesNo(default=True)
config.plugins.bisspro.match_name = ConfigYesNo(default=True)
config.plugins.bisspro.ignore_hd = ConfigYesNo(default=True)
config.plugins.bisspro.normalize_name = ConfigYesNo(default=True)
config.plugins.bisspro.cache_time = ConfigSelection(default="10", choices=[
    ("0", "Disable Cache"),
    ("5", "5 Minutes"),
    ("10", "10 Minutes"),
    ("30", "30 Minutes"),
    ("60", "60 Minutes"),
])
config.plugins.bisspro.backup_enable = ConfigYesNo(default=True)
config.plugins.bisspro.backup_keep = ConfigInteger(default=5, limits=(1, 50))
config.plugins.bisspro.confirm_delete = ConfigYesNo(default=True)
config.plugins.bisspro.language = ConfigSelection(default="en", choices=[
    ("en", "English"),
    ("ar", "Arabic")
])
config.plugins.bisspro.debug = ConfigYesNo(default=False)
config.plugins.bisspro.dry_run = ConfigYesNo(default=False)
