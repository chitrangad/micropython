

try:
  import socket as socket
except:
  import socket

from machine import Pin
import network
import os

import esp

esp.osdebug(None)

import gc
gc.collect()
print(gc.mem_free())

ssid = 'yourwifissid'
password = 'yourpassword'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

import webrepl

webrepl.start()


