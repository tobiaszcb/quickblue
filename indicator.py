import gi
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk
from gi.repository import AppIndicator3
from gi.repository import Notify

from typing import List
from os.path import  abspath

from device import Device

APP_INDICATOR_ID = "myAppIndicator"
APP_ICON = abspath("airpods_icon.png")


class Indicator:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(APP_INDICATOR_ID, APP_ICON, AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.menu = Gtk.Menu()

    def create_menu_items(self, devices: List[Device]) -> None:
        for device in devices:
            item = Gtk.MenuItem(device.name)
            item.connect("activate", self.connect_device, device)

            self.menu.append(item)

    def connect_device(self, source: Gtk.MenuItem, *data):
        device = data[0]

        if (device.connected):
            device.disconnect()
            self._notify_disconnection(device)
        else:
            device.connect()
            self._notify_connection(device)

    def _notify_connection(self, device: Device):
        Notify.Notification.new(f"{device.name} connected").show()

    def _notify_disconnection(self, device: Device):
        Notify.Notification.new(f"{device.name} disconnected").show()

    def start(self):
        Notify.init(APP_INDICATOR_ID)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu)

        self.menu.show_all()

        Gtk.main()