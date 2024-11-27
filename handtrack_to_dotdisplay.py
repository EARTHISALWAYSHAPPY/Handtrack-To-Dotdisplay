import mediapipe as mp
import cv2
from enum import Enum
import pandas as pd
import serial
import time

cv2.VideoCapture(0)
cam = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
# board_nanon = serial.Serial("COM5", 9600)

while True:
    frame, image = cam.read()
    if not frame:
        print("Your turn off webcam")
        break

    image = cv2.resize(image, (640, 480))
    image = cv2.flip(image, 1)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        # drawing joints & lines of hand_landmarks
        for hand_landmarks in result.multi_hand_landmarks:

            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=4),  # joints
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=4),  # lines
            )
        # Normalized pixel
        my_landmarks = [
            mp_hands.HandLandmark.WRIST,  # 0
            mp_hands.HandLandmark.THUMB_MCP,  # 2
            mp_hands.HandLandmark.THUMB_TIP,  # 4
            mp_hands.HandLandmark.INDEX_FINGER_PIP,  # 6s
            mp_hands.HandLandmark.INDEX_FINGER_TIP,  # 8
            mp_hands.HandLandmark.MIDDLE_FINGER_PIP,  # 10
            mp_hands.HandLandmark.MIDDLE_FINGER_TIP,  # 12
            mp_hands.HandLandmark.RING_FINGER_PIP,  # 14
            mp_hands.HandLandmark.RING_FINGER_TIP,  # 16
            mp_hands.HandLandmark.PINKY_PIP,  # 18
            mp_hands.HandLandmark.PINKY_TIP,  # 20
        ]
        data_landmark = {}
        image_height = image.shape[0]  # y-axis
        image_width = image.shape[1]  # x-axis
        for landmarks in mp_hands.HandLandmark:
            if landmarks in my_landmarks:
                x = hand_landmarks.landmark[landmarks].x * image_width
                y = hand_landmarks.landmark[landmarks].y * image_height
                data_landmark[landmarks.name] = {"X": x, "Y": y}
        # print("Data Landmark:", data_landmark)
        # time.sleep(1)
    cv2.imshow("Cam", image)

    if cv2.waitKey(1) & 0xFF == ord("e"):
        break


cam.release()
cv2.destroyAllWindows()
