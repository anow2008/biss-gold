# -*- coding: utf-8 -*-
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox

from Components.ActionMap import ActionMap
from Components.MenuList import MenuList

from .softcam import BISS_FILE
from .lang import L

import os


class SelectKeyScreen(Screen):
    skin = """<screen position="center,center" size="720,420" title="Manage Keys">
                <widget name="list" position="20,20" size="680,320"/>
              </screen>"""

    def __init__(self, session, sid, callback):
        Screen.__init__(self, session)
        self.sid = sid
        self.callback = callback

        self["list"] = MenuList([])
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
        items = []
        if os.path.exists(BISS_FILE):
            with open(BISS_FILE, "r", encoding="utf-8", errors="ignore") as f:
                for l in f:
                    p = l.strip().split()
                    if len(p) >= 4 and p[0].upper() == "F" and p[1].upper() == self.sid.upper():
                        items.append((l.strip(), l.strip()))

        if not items:
            self.session.open(
                MessageBox,
                L("NO_KEYS_FOR_SID"),
                MessageBox.TYPE_INFO,
                3
            )
            self.close()
            return

        self["list"].setList(items)

    def ok(self):
        sel = self["list"].getCurrent()
        self.close(sel[0] if sel else None)
