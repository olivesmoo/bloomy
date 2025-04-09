import time

#Bluetooth peripheral
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

#sensors
import board
import adafruit_scd4x
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C

reset_pin = None
i2c = board.STEMMA_I2C()

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

scd4x = adafruit_scd4x.SCD4X(i2c)
pm25 = PM25_I2C(i2c, reset_pin)

print("Serial number:", [hex(i) for i in scd4x.serial_number])
scd4x.start_periodic_measurement()
print("CLUE: Advertising BLE UART service")

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    print("CLUE: Connected")
    while ble.connected:
        time.sleep(1)
        if scd4x.data_ready:
            co2 = scd4x.CO2
            temp = scd4x.temperature
            humidity = scd4x.relative_humidity
            try:
                aqdata = pm25.read()
            except RuntimeError:
                print("Unable to read from sensor, retrying...")
                continue

            co2_msg = f"CO2: {co2} ppm, Temp: {temp:.1f} C, Humidity: {humidity:.1f}%\n"
            pmsa_msg = (
                "STD,{},{},{},".format(
                    aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"]
                )
                + "ENV,{},{},{},".format(
                    aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"]
                )
                + "P,{},{},{},{},{},{}\n".format(
                    aqdata["particles 03um"],
                    aqdata["particles 05um"],
                    aqdata["particles 10um"],
                    aqdata["particles 25um"],
                    aqdata["particles 50um"],
                    aqdata["particles 100um"],
                )
            )

            print(co2_msg)
            print(pmsa_msg)
            #uart.write(msg.encode("utf-8"))
            uart.write(b"Hello from CLUE!\n")
        time.sleep(1)
