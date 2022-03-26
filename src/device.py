import subprocess as sp

def list_devices():
    # ['Device 9C:64:8B:73:5D:39 Tobiasz’s AirPods', 'Device D0:D0:03:1F:3A:95 [TV] Samsung 7 Series (50)']
    result = sp.check_output(['bluetoothctl', 'devices']).decode("utf-8")

    # [['9C:64:8B:73:5D:39', 'Tobiasz’s AirPods'], ['D0:D0:03:1F:3A:95', '[TV] Samsung 7 Series (50)']]
    devices_attributes = [ d.replace('Device ', '').split(' ', 1) for d in result.splitlines() ]

    return [ Device(d[1], d[0]) for d in devices_attributes if "AirPods" in d[1] ]

class Device:
    def __init__(self, name, mac) -> None:
        self.name = name
        self.mac = mac

    def connect(self):
        sp.check_output(['bluetoothctl', 'connect', self.mac])

    def disconnect(self):
        sp.check_output(['bluetoothctl', 'disconnect', self.mac])

    @property
    def connected(self) -> bool:
        info_result_list = sp.check_output(['bluetoothctl', 'info', self.mac]).decode("utf-8").split()
        connected_attribute_index = info_result_list.index("Connected:")
        connected_value_index = connected_attribute_index + 1
        return info_result_list[connected_value_index] == 'yes'

def get_current_device() -> Device:
    for device in list_devices():
        if device.connected:
            return device