import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_crickit import crickit
from adafruit_motor import stepper

# Initialize BLE
ble = BLERadio()
print("Scanning for peripherals...")

# Initialize NeoPixels (once)
crickit.init_neopixel(12, bpp=4, pixel_order=(1, 0, 2, 3))
#crickit.init_neopixel(12)
# Define colors
color_for_particle = 0xff7c00
color_for_co2 = 0x002bff
color_for_bad = 0xff0000
crickit.neopixel.brightness = 0.3
color_for_good = 0xda33c1
# Initial motor/LED config
motor_speed = 0.10           # seconds between steps
motor_active = False
duration =  50                # duration motor runs after trigger
direction = stepper.FORWARD   # initial direction
prev_state = "bad"
cur_state = "bad"


while True:
    print("hello")
    # Idle indication
 #   crickit.neopixel.fill(color_for_bad)

   # crickit.neopixel.fill(color_for_bad)

    #crickit.onboard_pixel.fill((0,0, 0))

    for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):
        if UARTService in adv.services:
            print("Found a UART device:", adv.address)
            connection = ble.connect(adv)
            print("Connecting...")

            while not connection.connected:
               pass

            print("Connected")
            uart = connection[UARTService]
   #         try:
    #            connection = ble.connect(adv, timeout=10)
     #           print("Connecting...")
      #          uart = connection[UARTService]
       #         print("Connected")
        #    except ConnectionError as e:
         #       print("Connection failed:", e)
          #      continue

            # Wait for initial state message
            print("Waiting for initial state ('good' or 'bad')...")
            initial_state = None
            while connection.connected and not initial_state:
                if uart.in_waiting:
                    received = uart.readline().decode("utf-8").strip()
                    print("Received:", received)
                    initial_state = received
                    if received == "bad":
                        crickit.neopixel.fill(color_for_bad)
                        print("Initial state: BAD")
                        prev_state = "bad"
                    elif received == "co2":
                        crickit.neopixel.fill(color_for_co2)
                        print("Initial state: co2")
                        prev_state = "bad"
                    elif received == "particle":
                        crickit.neopixel.fill(color_for_particle)
                        print("Initial state: particle")
                        prev_state = "bad"
                    elif received == "good":
                        initial_state = "good"
                        motor_active = True
                        prev_state = "good"
                        motor_begins = time.monotonic()
                        direction = stepper.FORWARD
                        crickit.neopixel.fill(color_for_good)
                        print("Initial state: GOOD")

            # Main control loop
            led_index = 0
            last_motor_time = time.monotonic()
            print("hello?:")
            while connection.connected:
                now = time.monotonic()

                # Handle incoming UART messages
                if uart.in_waiting:
                    received = uart.readline().decode("utf-8").strip()
                    print("Received:", received)

                    if received == "bad":
                        crickit.neopixel.fill(color_for_bad)
                        cur_state = "bad"
                    elif received == "co2":
                        crickit.neopixel.fill(color_for_co2)
                        cur_state = "bad"
                    elif received == "particle":
                        crickit.neopixel.fill(color_for_particle)
                        cur_state = "bad"
                        print("P")
                    elif received == "good":
                        crickit.neopixel.fill(color_for_good)
                        cur_state = "good"
                    #crickit.neopixel.brightness = 0.3

                    if cur_state != prev_state:
                        motor_active = True
                        motor_begins = now
                        if received == "good":
                            direction = stepper.FORWARD
                            prev_state = "good"
                            print("open")
                        else:
                            direction = stepper.BACKWARD
                            prev_state = "bad"
                            print("close")

                # Step motor if active
               # print("now", now)
                #print("last_motor", last_motor_time)
                if motor_active and (now - last_motor_time >= motor_speed):
                    crickit.stepper_motor.onestep(direction=direction)
                    last_motor_time = now
                    print("motor is running")

                # Auto-stop motor after duration
                if motor_active and (now - motor_begins) >= duration:
                    print("Motor auto-stopped after duration")
                    motor_active = False
                    crickit.stepper_motor.release()


                time.sleep(0.01)

            print("Disconnected")
#except KeyboardInterrupt:
 #   print("Interrupted by user. Closing the flower...")
#finally:
 #   if prev_state != "bad":
  #  for _ in range(100):
   #     crickit.stepper_motor.onestep(direction=stepper.BACKWARD)
    #    time.sleep(motor_speed)
