#!/usr/bin/python3

from typing import List
from tendo import singleton

from device import Device, list_devices
from indicator import Indicator


AIRPODS: List[Device] = list_devices()

def main():
    indicator = Indicator()
    indicator.create_menu_items(AIRPODS)
    indicator.start()


if __name__ == "__main__":
    single_process = singleton.SingleInstance()
    main()