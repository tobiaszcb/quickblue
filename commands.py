import gi
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk

import subprocess as sp

class Device:
    def __init__(self, name, mac) -> None:
        self.name = name
        self.mac = mac

    def connect(self):
        pass

def quit_command():
    item_quit = gtk.MenuItem("Quit")
    item_quit.connect("activate", gtk.main_quit)
    return item_quit

def list_devices():
    # ['Device 9C:64:8B:73:5D:39 Tobiasz’s AirPods', 'Device D0:D0:03:1F:3A:95 [TV] Samsung 7 Series (50)']
    result = sp.check_output(['./scripts/list_devices.sh']).decode("utf-8")

    # [['9C:64:8B:73:5D:39', 'Tobiasz’s AirPods'], ['D0:D0:03:1F:3A:95', '[TV] Samsung 7 Series (50)']]
    devices_attributes = [d.replace('Device ', '').split(' ', 1) for d in result.splitlines()]
    
    return [ Device(d[1], d[0]) for d in devices_attributes ]

def connect_device():
    pass
