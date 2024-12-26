from gpiozero import Button
import os
import signal
import time

# GPIO pin for the button
BUTTON_PIN = 17
button = Button(BUTTON_PIN, pull_up=True)

# PID of the rpicam-still process
RPICAM_PID = None

# Function to read rpicam-still PID from the running process
def get_rpicam_pid():
    try:
        result = os.popen("ps aux | grep '[r]picam-still'").read().strip()
        if result:
            # Extract PID from the process details
            pid = result.split()[1]
            return int(pid)
        else:
            return None
    except ValueError:
        return None

# Function to send signal to rpicam-still
def capture_image():
    global RPICAM_PID
    if RPICAM_PID:
        print("Capturing image...")
        os.kill(RPICAM_PID, signal.SIGUSR1)
    else:
        print("Error: rpicam-still not running!")

# Detect button press
def on_button_pressed():
    print("Button pressed. Triggering capture...")
    capture_image()

# Detect button hold (to prevent continuous capture)
def wait_for_release():
    while button.is_pressed:
        time.sleep(1)

# Main function
def main():
    global RPICAM_PID
    RPICAM_PID = get_rpicam_pid()
    if RPICAM_PID is None:
        print("Error: rpicam-still is not running!")
        return

    print("Waiting for button press...")
    while True:
        button.wait_for_press()
        on_button_pressed()
        wait_for_release()

if __name__ == "__main__":
    main()
