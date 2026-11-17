from machine import Pin, UART
from neopixel import NeoPixel
import LCD
import time


# -----------------------------
# Hardware configuration
# -----------------------------

# GPS: UART0
gps = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Button on GP15, active LOW
button = Pin(15, Pin.IN, Pin.PULL_UP)

# One NeoPixel on GP12
pixel = NeoPixel(Pin(12), 1)

# Recording duration
RECORD_TIME = 10000  # milliseconds

# GPS speed conversion
KNOTS_TO_MPH = 1.15078


# -----------------------------
# LCD colors
# -----------------------------

BLACK = LCD.RGB(0, 0, 0)
WHITE = LCD.RGB(255, 255, 255)
GREEN = LCD.RGB(0, 255, 0)
BLUE = LCD.RGB(0, 0, 255)
RED = LCD.RGB(255, 0, 0)
YELLOW = LCD.RGB(255, 255, 0)


# -----------------------------
# Program variables
# -----------------------------

gps_buffer = ""

gps_time = "--:--:--"
current_speed = 0.0
gps_fix = False

# Top three speeds, highest first
leaderboard = []

# Recording variables
recording = False
record_start = 0
max_speed = 0.0

# Most recent run's rank
last_rank = 0
last_run_speed = 0.0

button_was_pressed = False
last_button_time = 0

last_display_update = 0


# -----------------------------
# NeoPixel functions
# -----------------------------

def set_pixel(rank):

    if rank == 1:
        pixel[0] = (0, 0, 255)       # Blue

    elif rank == 2:
        pixel[0] = (255, 0, 0)      # Red

    elif rank == 3:
        pixel[0] = (255, 255, 0)    # Yellow

    else:
        pixel[0] = (0, 0, 0)        # Off

    pixel.write()


# -----------------------------
# GPS parsing
# -----------------------------

def process_gps_line(line):

    global gps_time
    global current_speed
    global gps_fix

    # Remove whitespace
    line = line.strip()

    # Only process RMC sentences
    if not (line.startswith("$GPRMC") or
            line.startswith("$GNRMC")):
        return

    fields = line.split(",")

    if len(fields) < 8:
        return

    # Field 1: UTC time
    # Field 2: A = valid fix, V = invalid fix
    # Field 7: Speed in knots

    if len(fields[1]) >= 6:

        raw_time = fields[1]

        hours = raw_time[0:2]
        minutes = raw_time[2:4]
        seconds = raw_time[4:6]

        gps_time = hours + ":" + minutes + ":" + seconds

    if fields[2] == "A":

        gps_fix = True

        try:
            speed_knots = float(fields[7])
            current_speed = speed_knots * KNOTS_TO_MPH

        except:
            return

    elif fields[2] == "V":

        gps_fix = False
        current_speed = 0.0


def read_gps():

    global gps_buffer

    if gps.any():

        data = gps.read()

        if data:

            try:
                gps_buffer += data.decode("ascii")

            except:
                return

            # Process complete NMEA sentences
            while "\n" in gps_buffer:

                line, gps_buffer = gps_buffer.split("\n", 1)

                process_gps_line(line)


# -----------------------------
# Leaderboard functions
# -----------------------------

def update_leaderboard(new_speed):

    global leaderboard

    # Determine rank before inserting the new result.
    rank = 0

    for i in range(len(leaderboard)):

        if new_speed > leaderboard[i]:

            rank = i + 1
            break

        elif new_speed == leaderboard[i]:

            rank = i + 1
            break

    # If it is slower than all existing entries
    if rank == 0 and len(leaderboard) < 3:
        rank = len(leaderboard) + 1

    # Insert and sort
    leaderboard.append(new_speed)

    leaderboard.sort(reverse=True)

    # Keep only the top three
    leaderboard = leaderboard[:3]

    # If it did not make the top three, no rank
    if new_speed not in leaderboard:
        rank = 0

    return rank


# -----------------------------
# Recording functions
# -----------------------------

def start_recording():

    global recording
    global record_start
    global max_speed

    recording = True
    record_start = time.ticks_ms()

    if gps_fix:
        max_speed = current_speed
    else:
        max_speed = 0.0

    print("Recording started")


def finish_recording():

    global recording
    global last_rank
    global last_run_speed

    recording = False

    last_run_speed = max_speed

    # Only enter a run if GPS has provided a valid fix
    if not gps_fix:
        last_rank = 0
        set_pixel(0)
        print("Run discarded: GPS fix lost")
        return

    last_rank = update_leaderboard(max_speed)

    set_pixel(last_rank)

    print("Run complete")
    print("Maximum speed:", round(max_speed, 2), "mph")
    print("Rank:", last_rank)


# -----------------------------
# LCD functions
# -----------------------------

def initialize_display():

    LCD.Init()
    LCD.Clear(BLACK)

    LCD.Text("GPS SPEED RECORDER", 20, 15, GREEN, BLACK)

    LCD.Text("GPS TIME:", 20, 60, WHITE, BLACK)
    LCD.Text("CURRENT SPEED:", 20, 105, WHITE, BLACK)

    LCD.Text("RECORDING STATUS:", 20, 160, WHITE, BLACK)

    LCD.Text("TOP SPEEDS", 20, 215, GREEN, BLACK)

    LCD.Text("1ST:", 20, 250, WHITE, BLACK)
    LCD.Text("2ND:", 20, 275, WHITE, BLACK)
    LCD.Text("3RD:", 20, 300, WHITE, BLACK)


def update_display():

    global last_display_update

    # GPS time
    LCD.Text(gps_time, 180, 60, GREEN, BLACK)

    # Current speed
    if gps_fix:

        speed_string = "{:.1f} mph".format(current_speed)

    else:

        speed_string = "NO GPS FIX"

    LCD.Text(" " * 15, 180, 105, WHITE, BLACK)
    LCD.Text(speed_string, 180, 105, GREEN, BLACK)

    # Recording status
    if recording:

        elapsed = time.ticks_diff(
            time.ticks_ms(), record_start
        )

        remaining = max(0, RECORD_TIME - elapsed)

        status = "RECORDING: {}s".format(
            remaining // 1000
        )

    else:

        status = "PRESS GP15 TO START"

    LCD.Text(" " * 25, 180, 160, WHITE, BLACK)
    LCD.Text(status, 180, 160, YELLOW, BLACK)

    # Leaderboard
    for i in range(3):

        if i < len(leaderboard):

            speed_string = "{:.1f} mph".format(
                leaderboard[i]
            )

        else:

            speed_string = "--- mph"

        LCD.Text(" " * 15, 100, 250 + i * 25, WHITE, BLACK)
        LCD.Text(
            speed_string,
            100,
            250 + i * 25,
            GREEN,
            BLACK
        )

    # Most recent run
    if last_run_speed > 0:

        LCD.Text(
            "LAST RUN: {:.1f} mph".format(last_run_speed),
            250,
            250,
            WHITE,
            BLACK
        )

        if last_rank > 0:

            LCD.Text(
                "RANK: {}".format(last_rank),
                250,
                280,
                YELLOW,
                BLACK
            )

        else:

            LCD.Text(
                "OUTSIDE TOP 3",
                250,
                280,
                WHITE,
                BLACK
            )


# -----------------------------
# Main program
# -----------------------------

initialize_display()

set_pixel(0)

print("GPS Speed Recorder Ready")

while True:

    # Continuously read GPS
    read_gps()

    now = time.ticks_ms()

    # -------------------------
    # Button detection
    # -------------------------

    button_pressed = button.value() == 0

    if button_pressed and not button_was_pressed:

        if time.ticks_diff(now, last_button_time) > 250:

            last_button_time = now

            if not recording:
                start_recording()

    button_was_pressed = button_pressed

    # -------------------------
    # Track maximum speed
    # -------------------------

    if recording:

        if gps_fix:

            if current_speed > max_speed:
                max_speed = current_speed

        elapsed = time.ticks_diff(now, record_start)

        if elapsed >= RECORD_TIME:

            finish_recording()

    # -------------------------
    # Update LCD
    # -------------------------

    if time.ticks_diff(now, last_display_update) >= 500:

        last_display_update = now

        update_display()

    # Short pause; GPS is still read continuously
    time.sleep_ms(5)