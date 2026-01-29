# -*- coding: utf-8 -*-
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox

from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Label import Label

from .config import config
from .paths import PLUGIN_VERSION, PLUGIN_BUILD
from .lang import L

from .screens_about import AboutScreen


class SettingsScreen(Screen):
    skin = """<screen position="center,center" size="720,520" title="BissPro Settings">
                <widget name="list" position="20,20" size="680,430" scrollbarMode="showOnDemand"/>
                <widget name="version" position="20,460" size="680,40" font="Regular;22" halign="center"/>
              </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self["list"] = MenuList([])
        self["version"] = Label(
            "Version: %s   Build: %s" % (PLUGIN_VERSION, PLUGIN_BUILD)
        )
        self["actions"] = ActionMap(
            ["OkCancelActions"],
            {
                "ok": self.ok,
                "cancel": self.close
            },
            -1
        )
        self.load()

    def load(self):
        items = [
            ("%s: %s" % (L("RESTART_MODE"), config.plugins.bisspro.restart_mode.value), "restart_mode"),
            ("%s: %s" % (L("MATCH_SID"), "On" if config.plugins.bisspro.match_sid.value else "Off"), "match_sid"),
            ("%s: %s" % (L("MATCH_NAME"), "On" if config.plugins.bisspro.match_name.value else "Off"), "match_name"),
            ("%s: %s" % (L("IGNORE_HD"), "On" if config.plugins.bisspro.ignore_hd.value else "Off"), "ignore_hd"),
            ("%s: %s" % (L("NORMALIZE_NAME"), "On" if config.plugins.bisspro.normalize_name.value else "Off"), "normalize_name"),
            ("%s: %s" % (L("CACHE_TIME"), config.plugins.bisspro.cache_time.value + " min"), "cache_time"),
            ("%s: %s" % (L("BACKUP_ENABLE"), "On" if config.plugins.bisspro.backup_enable.value else "Off"), "backup_enable"),
            ("%s: %s" % (L("BACKUP_KEEP"), str(config.plugins.bisspro.backup_keep.value)), "backup_keep"),
            ("%s: %s" % (L("CONFIRM_DELETE_OPT"), "On" if config.plugins.bisspro.confirm_delete.value else "Off"), "confirm_delete"),
            ("%s: %s" % (L("LANGUAGE"), config.plugins.bisspro.language.value), "language"),
            ("%s: %s" % (L("DEBUG"), "On" if config.plugins.bisspro.debug.value else "Off"), "debug"),
            ("%s: %s" % (L("DRY_RUN"), "On" if config.plugins.bisspro.dry_run.value else "Off"), "dry_run"),
            (L("ABOUT"), "about"),
        ]
        self["list"].setList(items)

    def ok(self):
        sel = self["list"].getCurrent()
        if not sel:
            return

        key = sel[0][1]

        if key == "about":
            self.session.open(AboutScreen)
            return

        if key == "restart_mode":
            config.plugins.bisspro.restart_mode.value = (
                "full" if config.plugins.bisspro.restart_mode.value == "smart" else "smart"
            )

        elif key == "match_sid":
            config.plugins.bisspro.match_sid.value = not config.plugins.bisspro.match_sid.value

        elif key == "match_name":
            config.plugins.bisspro.match_name.value = not config.plugins.bisspro.match_name.value

        elif key == "ignore_hd":
            config.plugins.bisspro.ignore_hd.value = not config.plugins.bisspro.ignore_hd.value

        elif key == "normalize_name":
            config.plugins.bisspro.normalize_name.value = not config.plugins.bisspro.normalize_name.value

        elif key == "cache_time":
            order = ["0", "5", "10", "30", "60"]
            idx = order.index(config.plugins.bisspro.cache_time.value)
            config.plugins.bisspro.cache_time.value = order[(idx + 1) % len(order)]

        elif key == "backup_enable":
            config.plugins.bisspro.backup_enable.value = not config.plugins.bisspro.backup_enable.value

        elif key == "backup_keep":
            config.plugins.bisspro.backup_keep.value = min(
                50, config.plugins.bisspro.backup_keep.value + 1
            )

        elif key == "confirm_delete":
            config.plugins.bisspro.confirm_delete.value = not config.plugins.bisspro.confirm_delete.value

        elif key == "language":
            config.plugins.bisspro.language.value = (
                "ar" if config.plugins.bisspro.language.value == "en" else "en"
            )
            self.session.open(
                MessageBox,
                L("RESTART_GUI"),
                MessageBox.TYPE_INFO,
                3
            )

        elif key == "debug":
            config.plugins.bisspro.debug.value = not config.plugins.bisspro.debug.value

        elif key == "dry_run":
            config.plugins.bisspro.dry_run.value = not config.plugins.bisspro.dry_run.value

        self.load()
