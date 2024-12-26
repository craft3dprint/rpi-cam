#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to display a progress bar
progress_bar() {
    local duration=$1
    local progress=0
    local steps=50  # Number of steps in the progress bar
    local step_duration=$((duration / steps))
    
    echo -n "["
    for ((i = 0; i < steps; i++)); do
        sleep "$step_duration"
        echo -n "#"
        progress=$((progress + 1))
    done
    echo "]"
}

# Function to handle errors
error_exit() {
    echo "Error: $1"
    exit 1
}

# Main script
echo "Downloading....."
progress_bar 5
git clone https://github.com/craft3dprint/rpi-cam.git || error_exit "Failed to clone repository"

echo "Installing......"
progress_bar 8
cp rpi-cam/cam/capture_images.sh /usr/local/bin/ || error_exit "Failed to copy capture_images.sh"
cp rpi-cam/cam/button_trigger.py /home/$USER/button_trigger.py || error_exit "Failed to copy button_trigger.py"
cp rpi-cam/cam/rpicam-still.service /etc/systemd/system/ || error_exit "Failed to copy rpicam-still.service"

systemctl enable rpicam-still.service || error_exit "Failed to enable rpicam-still.service"
systemctl start rpicam-still.service || error_exit "Failed to start rpicam-still.service"

cp rpi-cam/web-app /home/$USER/ || error_exit "Failed to copy web-app"
cp rpi-cam/web-app/file-manager.service /etc/systemd/system/ || error_exit "Failed to copy file-manager.service"

systemctl enable file-manager.service || error_exit "Failed to enable file-manager.service"
systemctl start file-manager.service || error_exit "Failed to start file-manager.service"

rm -rf rpi-cam || error_exit "Failed to clean up repository"

echo "Installation completed successfully!"
