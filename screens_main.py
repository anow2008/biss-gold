# -*- coding: utf-8 -*-
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox

from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Label import Label
from Components.MultiContent import (
    MultiContentEntryPixmapAlphaTest,
    MultiContentEntryText
)

from enigma import iServiceInformation, gFont, eTimer
from Tools.LoadPixmap import LoadPixmap

from threading import Thread
import os, shutil

from .screens_settings import SettingsScreen
from .screens_easyinput import EasyBissInput
from .screens_select import SelectKeyScreen

from .paths import ICON_PATH, UPDATE_URL
from .config import config
from .lang import L
from .utils import create_backup
from .softcam import BISS_FILE, restartSoftcam
from .network import urlretrieve
from .auto_biss import import_biss_from_github


class BISSPro(Screen):
    skin = """<screen position="center,center" size="1024,768" title="BissPro Manager">
                <widget name="menu" position="40,100" size="940,540" itemHeight="150" scrollbarMode="showOnDemand"/>
                <widget name="status" position="40,650" size="940,50" font="Regular;28" halign="center" valign="center" foregroundColor="#00ff00"/>
              </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)

        self.menu_items = [
            (L("ADD_KEY"), "add", "add.png"),
            (L("EDIT_KEY"), "edit", "edit.png"),
            (L("DELETE_KEY"), "delete", "delete.png"),
            (L("UPDATE_SOFTCAM"), "update", "update.png"),
            (L("AUTO_ADD"), "auto_add", "auto_add.png"),
            (L("SETTINGS"), "settings", "settings.png"),
        ]

        self.menu_list = [
            (
                a,
                [
                    MultiContentEntryPixmapAlphaTest(
                        pos=(10, 10),
                        size=(128, 128),
                        png=LoadPixmap(ICON_PATH + i)
                    ),
                    MultiContentEntryText(
                        pos=(160, 50),
                        size=(760, 60),
                        font=0,
                        text=t
                    )
                ]
            )
            for t, a, i in self.menu_items
        ]

        self["menu"] = MenuList(self.menu_list)
        self["menu"].l.setFont(0, gFont("Regular", 32))
        self["status"] = Label("")

        self["actions"] = ActionMap(
            ["OkCancelActions", "DirectionActions"],
            {
                "ok": self.ok,
                "cancel": self.close,
                "up": self["menu"].up,
                "down": self["menu"].down
            },
            -1
        )

    def ok(self):
        sel = self["menu"].getCurrent()
        service = self.session.nav.getCurrentService()
        if not sel or not service:
            return

        action, info = sel[0], service.info()
        sid = "%08X" % info.getInfo(iServiceInformation.sSID)
        sname = info.getName().replace(" ", "_")

        if action == "add":
            self.session.open(EasyBissInput, sid, "add", None, sname)

        elif action in ("edit", "delete"):
            self.session.openWithCallback(
                lambda l: self.handle(action, sid, l, sname),
                SelectKeyScreen,
                sid,
                lambda x: x
            )

        elif action == "update":
            self.start_bg(lambda: self.bg_update(BISS_FILE), L("UPDATING"))

        elif action == "auto_add":
            self.start_bg(lambda: self.bg_auto(service), L("SEARCHING"))

        elif action == "settings":
            self.session.open(SettingsScreen)

    def start_bg(self, target, msg):
        self["status"].setText(msg)
        Thread(target=target).start()

    def bg_update(self, dest):
        try:
            create_backup()
            urlretrieve(UPDATE_URL, "/tmp/sc.tmp")
            if os.path.exists("/tmp/sc.tmp"):
                shutil.copy("/tmp/sc.tmp", dest)
            if not config.plugins.bisspro.dry_run.value:
                restartSoftcam()
            self.done(True, L("SOFTCAM_UPDATED"))
        except:
            self.done(False, L("DOWNLOAD_FAILED"))

    def bg_auto(self, service):
        ok, msg = import_biss_from_github(service)
        self.done(ok, msg)

    def done(self, ok, msg):
        self.res = (ok, msg)
        eTimer.singleShot(100, self.show_res)

    def show_res(self):
        self["status"].setText("")
        self.session.open(
            MessageBox,
            self.res[1],
            MessageBox.TYPE_INFO if self.res[0] else MessageBox.TYPE_ERROR,
            3
        )

    def handle(self, action, sid, line, sname):
        if not line:
            return
        if action == "edit":
            self.session.open(EasyBissInput, sid, "edit", line, sname)
        else:
            if config.plugins.bisspro.confirm_delete.value:
                self.session.openWithCallback(
                    lambda c: self.del_k(c, line),
                    MessageBox,
                    L("CONFIRM_DELETE"),
                    MessageBox.TYPE_YESNO
                )
            else:
                self.del_k(True, line)

    def del_k(self, conf, line):
        if not conf:
            return
        create_backup()
        with open(BISS_FILE, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        with open(BISS_FILE, "w", encoding="utf-8", errors="ignore") as f:
            done = False
            for l in lines:
                if not done and l.strip() == line.strip():
                    done = True
                    continue
                f.write(l)
        if not config.plugins.bisspro.dry_run.value:
            restartSoftcam()
        self.session.open(MessageBox, L("KEY_DELETED"), MessageBox.TYPE_INFO, 3)
