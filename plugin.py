# -*- coding: utf-8 -*-
from Plugins.Plugin import PluginDescriptor
from .paths import PLUGIN_NAME
from .screens_main import BISSPro

def main(session, **kwargs):
    session.open(BISSPro)

def Plugins(**kwargs):
    return [
        PluginDescriptor(
            name=PLUGIN_NAME,
            description="Pro BISS Keys Manager",
            where=PluginDescriptor.WHERE_PLUGINMENU,
            fnc=main,
            icon="plugin.png"
        )
    ]
