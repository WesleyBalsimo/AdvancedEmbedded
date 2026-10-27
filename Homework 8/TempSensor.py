from machine import Pin
from time import sleep_ms, ticks_ms, ticks_diff
import ds18x20
import onewire
import os

# Sensor setup
ds_pin = Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()
print('Found DS devices:', roms)

# Button setup
startPin = Pin(15, Pin.IN, Pin.PULL_UP)

# Recording settings
DURATION = 60  # seconds

if not roms:
    raise RuntimeError("No DS18B20 sensor found")

# Find next available filename
def get_filename():
    run = 1

    while "run{}.txt".format(run) in os.listdir():
        run += 1

    return "run{}.txt".format(run)


while True:

    print("Waiting for button press...")

    # Wait for button press
    while startPin.value() == 1:
        sleep_ms(10)

    # Debounce
    sleep_ms(50)

    if startPin.value() != 0:
        continue

    # Generate filename
    FILENAME = get_filename()

    print("Recording started:", FILENAME)

    # Create new file
    with open(FILENAME, "w") as file:

        file.write("Time_s Temperature_C\n")

        start_time = ticks_ms()

        while ticks_diff(ticks_ms(), start_time) < DURATION * 1000:

            ds_sensor.convert_temp()
            sleep_ms(1000)

            Temp = ds_sensor.read_temp(roms[0])
            elapsed = ticks_diff(ticks_ms(), start_time) / 1000

            # Save data
            file.write("{:.3f} {:.4f}\n".format(elapsed, Temp))
            file.flush()

            # Print to terminal
            print("Time: {:.3f}s, Temp: {:.4f}C".format(elapsed, Temp))

    print("Recording complete!")
    print("Data saved to:", FILENAME)

    # Wait for button release before next recording
    while startPin.value() == 0:
        sleep_ms(10)