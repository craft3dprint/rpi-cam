#!/bin/bash

BASE_DIR="/home/cam/3d-printer-pic"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
FOLDER="$BASE_DIR/$TIMESTAMP"
COUNT=1

# Create a unique folder
while [ -d "$FOLDER" ]; do
    FOLDER="$BASE_DIR/${TIMESTAMP}_$COUNT"
    ((COUNT++))
done
mkdir -p "$FOLDER"

echo "Created folder: $FOLDER"

# Start rpicam-still
rpicam-still -t 0 -s -o "$FOLDER/image_%04d.jpg" --width 1080 --height 1920 --nopreview --tuning-file /usr/share/libcamera/ipa/rpi/vc4/imx219_noir.json &
RPICAM_PID=$!

echo "rpicam-still started with PID $RPICAM_PID"
