# Hand-Gesture-Drone-And-Wireless-Charging-Station
This project enables control of a drone using hand gestures tracked via a webcam and QR code detection for specific actions like landing. 

The system employs computer vision, MediaPipe for hand tracking, and pyzbar for QR code recognition. 

It integrates with Arduino to send control commands to the drone.

## Features
- **Hand Gesture Control:** Detects hand movements to command the drone to move up, down, left, or right.
- **QR Code Detection:** Recognizes QR codes to trigger actions like landing.
- **Arduino Integration:** Sends serial commands to the drone via an Arduino board.
- **Cooldown Mechanism:** Prevents repeated commands within a short timeframe to ensure smooth operation.

## Technologies Used
- **Python Libraries:**
  - OpenCV: For video capture and processing.
  - MediaPipe: For hand tracking and landmark detection.
  - pyzbar: For QR code decoding.
  - Serial: For communication with the Arduino board.
  - NumPy: For numerical computations.
- **Hardware:**
  - Webcam: To capture video for processing.
  - Arduino: To send commands to the drone.

## Installation and Setup
### Prerequisites
1. Python 3.10 installed.
2. Install required libraries:
**pip install opencv-python opencv-contrib-python imutils mediapipe pyzbar pyserial numpy**
3. An Arduino board connected to the appropriate COM port.
##How It Works
###Hand Gesture Detection
1. Uses MediaPipe to detect hand landmarks and calculates the center of the hand bounding box.
2. Determines movement direction (left, right, up, down) based on the change in hand position.
3. Sends corresponding commands to the Arduino.

###QR Code Detection
1. Detects QR codes in the video feed using pyzbar.
2. If a QR code with the message "Land Here For Charge Your Drone" is detected, the system triggers the landing command.

###Arduino Communication
1. Commands are sent to the Arduino via serial communication.
2. Arduino processes these commands to control the drone.
