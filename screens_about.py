# -*- coding: utf-8 -*-
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label

from .paths import PLUGIN_VERSION, PLUGIN_BUILD, PLUGIN_CHANGELOG


class AboutScreen(Screen):
    skin = """<screen position="center,center" size="720,420" title="About BissPro">
                <widget name="text" position="20,20" size="680,380" font="Regular;22" />
              </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self["text"] = Label(self.build_text())
        self["actions"] = ActionMap(
            ["OkCancelActions"],
            {
                "ok": self.close,
                "cancel": self.close
            },
            -1
        )

    def build_text(self):
        txt = "BissPro Manager\n"
        txt += "Version: %s\n" % PLUGIN_VERSION
        txt += "Build: %s\n\n" % PLUGIN_BUILD
        txt += "Changelog:\n"
        for line in PLUGIN_CHANGELOG:
            txt += "%s\n" % line
        return txt

