# -*- coding: utf-8 -*-
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox

from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Label import Label

from .softcam import BISS_FILE, restartSoftcam
from .utils import create_backup
from .config import config
from .lang import L

import os


class EasyBissInput(Screen):
    skin = """<screen position="center,center" size="820,300" title="Manual BISS Entry">
                <widget name="key" position="110,100" size="600,80"
                        font="Console;50" halign="center" valign="center"
                        foregroundColor="#ffffff"/>
                <widget name="hexlist" position="720,100" size="80,200" itemHeight="40"/>
              </screen>"""

    def __init__(self, session, sid, mode="add", key_line=None, sname="Unknown"):
        Screen.__init__(self, session)
        self.sid = sid
        self.mode = mode
        self.key_line = key_line
        self.sname = sname

        self.key = list("0000000000000000")
        self.pos = 0
        self.allchars = list("0123456789ABCDEF")

        if key_line:
            p = key_line.split()
            if len(p) >= 4 and len(p[3]) == 16:
                self.key = list(p[3])

        self["key"] = Label("")
        self["hexlist"] = MenuList([(c, c) for c in "ABCDEF"])

        self["actions"] = ActionMap(
            ["DirectionActions", "NumberActions", "ColorActions", "OkCancelActions"],
            {
                "left": self.left,
                "right": self.right,
                "up": self.up,
                "down": self.down,
                "ok": self.select_hex,
                "green": self.save,
                "cancel": self.close,
                **{str(i): (lambda x=str(i): self.set_num(x)) for i in range(10)}
            },
            -1
        )

        self.refresh()

    def refresh(self):
        self["key"].setText(
            "".join(
                "[%s]" % c if i == self.pos else " %s " % c
                for i, c in enumerate(self.key)
            )
        )

    def left(self):
        self.pos = (self.pos - 1) % 16
        self.refresh()

    def right(self):
        self.pos = (self.pos + 1) % 16
        self.refresh()

    def up(self):
        self.key[self.pos] = self.allchars[
            (self.allchars.index(self.key[self.pos]) + 1) % 16
        ]
        self.right()

    def down(self):
        self.key[self.pos] = self.allchars[
            (self.allchars.index(self.key[self.pos]) - 1) % 16
        ]
        self.right()

    def set_num(self, c):
        self.key[self.pos] = c
        self.right()

    def select_hex(self):
        sel = self["hexlist"].getCurrent()
        if sel:
            self.key[self.pos] = sel[0]
            self.right()

    def save(self):
        new_line = "F %s 00000000 %s ;%s" % (
            self.sid,
            "".join(self.key),
            self.sname
        )

        create_backup()

        lines = []
        if os.path.exists(BISS_FILE):
            with open(BISS_FILE, "r", encoding="utf-8", errors="ignore") as f:
                lines = [l.rstrip() for l in f]

        with open(BISS_FILE, "w", encoding="utf-8") as f:
            for l in lines:
                if self.mode == "edit" and self.key_line and l.strip() == self.key_line.strip():
                    continue
                if l.strip():
                    f.write(l + "\n")
            f.write(new_line + "\n")

        if not config.plugins.bisspro.dry_run.value:
            restartSoftcam()

        self.session.open(
            MessageBox,
            L("KEY_SAVED"),
            MessageBox.TYPE_INFO,
            3
        )
        self.close()
