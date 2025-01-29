# Raspberry Pi Audio-Video Recording System

This Python script controls a simple recording setup using a Raspberry Pi. The system records both video and audio, then combines them into a final video file (MP4). It uses a button to start/stop recording, with LEDs indicating the current status.

## Features

- **Start Recording**: Press the button to start recording both video and audio.
- **Stop Recording**: Press the button again to stop the recording and save the files.
- **Combine Audio and Video**: After stopping, the system merges the audio and video into a single MP4 file using `ffmpeg`.
- **LED Indicators**: 
  - **Green LED**: Ready to start recording.
  - **Red LED**: Recording in progress.
  - **Yellow LED**: Recording stopped, processing.

## Hardware Requirements

- **Raspberry Pi** with GPIO pins.
- **Raspberry Pi Camera** (compatible with `picamera2` library).
- **Microphone** or audio input device.
- **Button** (connected to GPIO pin 3).
- **3 LEDs** (connected to GPIO pins 17, 22, and 27).
- **`ffmpeg`** installed for video/audio processing.

## Installation and Setup

1. **Install required libraries**:
   ```bash
   pip install pyaudio picamera2 gpiozero
   sudo apt install ffmpeg


Enable Raspberry Pi Camera:

Run raspi-config and enable the camera.
Wiring the Hardware:

Button: Connect the button to GPIO pin 3.
LEDs: Connect 3 LEDs to GPIO pins 17 (Red), 22 (Yellow), and 27 (Green).
Run the script:

Execute the Python script, and use the button to control the recording process.
How It Works
Initial State:

The Green LED indicates the system is ready to start recording.
Start Recording:

Press the button to start recording.
The Red LED lights up, indicating that recording has begun. Video and audio are being captured simultaneously.
Stop Recording:

Press the button again to stop the recording.
The Yellow LED lights up, and the system processes the media, combining the audio and video into one file.
Final Output:

After the processing, the output file is saved as output_video.mp4 in the videos folder.
Troubleshooting
If the video does not play correctly, make sure ffmpeg is installed and properly configured on your Raspberry Pi.
Ensure the microphone is connected and accessible by the Raspberry Pi.
Check GPIO connections to make sure the button and LEDs are wired correctly.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
This project makes use of the following libraries:
pyaudio for audio recording.
picamera2 for video recording.
gpiozero for GPIO control.
ffmpeg for video and audio merging.
