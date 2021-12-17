#!/usr/bin/python3

from os.path import abspath
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as app_indicator

from commands import quit_command, list_devices

APP_INDICATOR_ID = "myAppIndicator"
APP_ICON = abspath("airpods_icon.png")

def init_indicator():
    indicator = app_indicator.Indicator.new(APP_INDICATOR_ID, APP_ICON, app_indicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(app_indicator.IndicatorStatus.ACTIVE)
    return indicator


def main():
    indicator = init_indicator()
    menu = gtk.Menu()

    devices = list_devices()
    for device in devices:
        item = gtk.MenuItem(device.name)
        item.connect("activate", gtk.main_quit)
        menu.append(item)



    menu.show_all()
    indicator.set_menu(menu)

    gtk.main()


if __name__ == "__main__":
    main()