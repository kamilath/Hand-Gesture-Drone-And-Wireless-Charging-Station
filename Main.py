import cv2
import mediapipe as mp
import numpy as np
from pyzbar.pyzbar import decode
import serial
import time

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  # Track only one hand
mp_drawing = mp.solutions.drawing_utils

# Initialize previous center coordinates
prev_center_x, prev_center_y = None, None

# Open serial port (Make sure the correct port is selected)
arduino = serial.Serial('COM3', 115200)  # Change 'COM3' to the appropriate port
time.sleep(2)  # Allow Arduino time to reset after the connection

# Start capturing from webcam
cap = cv2.VideoCapture(0)

# Track the last time each command was sent (for cooldown purposes)
last_command_time = {
    'Up': 0,
    'Down': 0,
    'Left': 0,
    'Right': 0
}

cooldown_interval = 5  # 1 seconds cooldown for each command

qrstat=""
while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    if not ret:
        break

    # Get the height and width of the frame
    h, w, _ = frame.shape

    # Convert the image to RGB format for MediaPipe
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # QR Code detection (using pyzbar)
    qr_codes = decode(frame)
    for qr in qr_codes:
        # Get the QR code data (decoded as a string)
        qr_data = qr.data.decode('utf-8')

        # Draw the bounding box around the QR code
        points = qr.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        else:
            # If the QR code is malformed or rotated, handle the case
            cv2.circle(frame, (qr.rect[0], qr.rect[1]), 5, (255, 0, 0), -1)

        # Check if the QR code contains the target string "Land Here For Charge Your Drone"
        if qr_data == "Land Here For Charge Your Drone" and qrstat!="Land":
            qrstat="Land"
            print("QR Detected: Land Your Drone Here")
            cv2.putText(frame, 'QR Detected: Land Your Drone Here', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # Send "landed" to Arduino
            arduino.write('Land'.encode())
            last_command_time['Land'] = time.time()  # Reset the cooldown for "Land" command

    # Process the frame with hand tracking
    results = hands.process(image)

    if results.multi_hand_landmarks:  # If hands are detected
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks and connections
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the bounding box for the hand
            min_x = min([landmark.x for landmark in hand_landmarks.landmark])
            max_x = max([landmark.x for landmark in hand_landmarks.landmark])
            min_y = min([landmark.y for landmark in hand_landmarks.landmark])
            max_y = max([landmark.y for landmark in hand_landmarks.landmark])

            # Convert normalized coordinates to pixel values
            min_x, max_x = int(min_x * w), int(max_x * w)
            min_y, max_y = int(min_y * h), int(max_y * h)

            # Calculate the center of the bounding box
            center_x = (min_x + max_x) // 2
            center_y = (min_y + max_y) // 2

            # Draw a rectangle around the hand
            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)  # Red dot for center

            # Skip the movement detection logic if prev_center_x or prev_center_y is None (first frame)
            if prev_center_x is not None and prev_center_y is not None:
                current_time = time.time()

                # Left and right movement detection based on center_x
                if center_x < prev_center_x - 30:  # Hand moved left
                    if current_time - last_command_time['Left'] > cooldown_interval:  # If cooldown has passed
                        print("Left")
                        arduino.write('Left'.encode())
                        last_command_time['Left'] = current_time  # Update cooldown for Left command
                    else:
                        print("Left detected but ignored due to cooldown")

                elif center_x > prev_center_x + 30:  # Hand moved right
                    if current_time - last_command_time['Right'] > cooldown_interval:  # If cooldown has passed
                        print("Right")
                        arduino.write('Right'.encode())
                        last_command_time['Right'] = current_time  # Update cooldown for Right command
                    else:
                        print("Right detected but ignored due to cooldown")

                # Up and down movement detection based on center_y
                if center_y < prev_center_y - 30:  # Hand moved up
                    if current_time - last_command_time['Up'] > cooldown_interval:  # If cooldown has passed
                        print("Up")
                        qrstat=""
                        arduino.write('Up'.encode())
                        last_command_time['Up'] = current_time  # Update cooldown for Up command
                    else:
                        print("Up detected but ignored due to cooldown")

                elif center_y > prev_center_y + 30:  # Hand moved down
                    if current_time - last_command_time['Down'] > cooldown_interval:  # If cooldown has passed
                        print("Down")
                        
                        arduino.write('Land'.encode())
                        last_command_time['Down'] = current_time  # Update cooldown for Down command
                    else:
                        print("Down detected but ignored due to cooldown")

            # Update previous positions for the next frame
            prev_center_x, prev_center_y = center_x, center_y

    # Display the processed frame with hand detection and QR code info
    cv2.imshow('Hand and QR Detection', frame)

    # Quit when the ESC key (ASCII 27) is pressed
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()

# Close the serial connection
arduino.close()
