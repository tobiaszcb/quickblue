from device import Device
from globals import APP_INDICATOR_ID

from typing import List
import gi
gi.require_version('Notify', '0.7')

from gi.repository import Notify


class Notifier:

    def __init__(self):
        Notify.init(APP_INDICATOR_ID)

    def connected(self, device: Device):
        Notify.Notification.new(f"{device.name} connected").show()

    def disconnected(self, device: Device):
        Notify.Notification.new(f"{device.name} disconnected").show()

    def discovered(self, devices: List[Device]):
        if not devices:
            body = "No devices discovered"
        elif len(devices) == 1:
            body = f"{devices[0].name} discovered"
        else:
            body = f", ".join([device.name for device in devices])

        Notify.Notification.new(body).show()