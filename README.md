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
1. Python 3.x installed.
2. Install required libraries:
   ```bash
   pip install opencv-python mediapipe pyzbar pyserial numpy
