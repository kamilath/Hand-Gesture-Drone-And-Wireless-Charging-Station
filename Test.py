import cv2
import mediapipe as mp
import numpy as np


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  
mp_drawing = mp.solutions.drawing_utils


def count_fingers(landmarks):
    
    finger_tips = [8, 12, 16, 20]  

    # Count the number of fingers that are up
    fingers_up = 0
    # Check if thumb is up
    if landmarks[4].x < landmarks[2].x: 
        fingers_up += 1
    # Check other fingers
    for tip in finger_tips:
        # Check if the finger tip is above its base joint
        if landmarks[tip].y < landmarks[tip - 2].y:
            fingers_up += 1
    return fingers_up


cap = cv2.VideoCapture(0) 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the image to RGB format
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Process the frame with hand tracking
    results = hands.process(image)

   
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks and connections
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Count fingers
            num_fingers = count_fingers(hand_landmarks.landmark)
            # Display the count on the frame
            cv2.putText(frame, f'Fingers Up: {num_fingers}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
            
    cv2.imshow('Finger Counter', frame)
    

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
