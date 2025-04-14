import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_crickit import crickit
from adafruit_motor import stepper

# Initialize BLE
ble = BLERadio()
print("Scanning for peripherals...")

# Initialize NeoPixels on Crickit (once!)
crickit.init_neopixel(12, bpp=4, pixel_order=(1, 0, 2, 3))

while True:

    for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):
        if UARTService in adv.services:
            print("Found a UART device:", adv.address)
            connection = ble.connect(adv)
            print("Connecting...")

            while not connection.connected:
                pass  # Wait until fully connected

            print("Connected")
            uart = connection[UARTService]

            while connection.connected:
                if uart.in_waiting:
                    received = uart.readline().decode("utf-8").strip()
                    print("Received:", received)

                    if received == "Hello from CLUE!":
                        print("Starting motor + NeoPixel loop!")
                        time.sleep(30)
                        crickit.stepper_motor.onestep(direction=stepper.FORWARD)
                        time.sleep(30)
                time.sleep(30)



            print("Disconnected")
