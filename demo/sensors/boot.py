import machine
import network

SSID = ""
PASSWORD = ""

wlan = network.WLAN()
wlan.active(True)
if not wlan.isconnected():
    print(f"Connecting to {SSID}...")
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        machine.idle()
    print("Connected!")
