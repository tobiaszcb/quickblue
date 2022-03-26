import gi
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk
from gi.repository import AppIndicator3

from typing import List

from device import Device, list_devices
from notifications import Notifier
from globals import *


class Indicator:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(APP_INDICATOR_ID, APP_ICON, AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.menu = Gtk.Menu()
        self.notifier = Notifier()

    def start(self):
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu)

        self.menu.show_all()

        Gtk.main()

    def add_devices(self, devices: List[Device]):
        for device in devices:
            item = Gtk.MenuItem(device.name)
            item.connect("activate", self.connect_device, device)
            self.menu.append(item)

    # TODO: change method name
    def connect_device(self, source: Gtk.MenuItem, *data):
        device = data[0]

        if (device.connected):
            device.disconnect()
            self.notifier.disconnected(device)
        else:
            device.connect()
            self.notifier.connected(device)

    def rediscover_items(self, source: Gtk.MenuItem):
        self.remove_existing_items()

        devices = list_devices()
        self.notifier.discovered(devices)

        self.add_devices(devices)
        self.create_standard_menu()

        self.menu.show_all()

    def disconnect(self, source: Gtk.MenuItem, *data):
        current_device = next(device for device in list_devices() if device.connected)
        if current_device:
            current_device.disconnect()
        Gtk.main_quit()

    def remove_existing_items(self):
        children: List[Gtk.MenuItem] = self.menu.get_children()
        if children:
            for child in children:
                self.menu.remove(child)

    def create_standard_menu(self):
        self._create_separator_item()
        self._create_discover_item()
        self._create_quit_item()

    def _create_separator_item(self):
        separator = Gtk.SeparatorMenuItem()
        self.menu.append(separator)
        separator.show()

    def _create_discover_item(self):
        discover_item = Gtk.MenuItem("Discover")
        discover_item.connect("activate", self.rediscover_items)
        self.menu.append(discover_item)

    def _create_quit_item(self):
        quit_item = Gtk.MenuItem("Quit")
        quit_item.connect("activate", self.disconnect)
        self.menu.append(quit_item)