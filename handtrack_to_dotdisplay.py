import mediapipe as mp
import cv2
import serial
import time

cv2.VideoCapture(0)  # select my webcam
cam = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils  # joints and line
# board_nanon = serial.Serial("COM5", 9600)


def look_a_like(
    wrist_y, thumb_tip_y, index_tip_y, middle_tip_y, ring_tip_y, pinky_tip_y
):
    if thumb_tip_y < wrist_y:
        cv2.putText(
            image, "Very good", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )
        output = "A"

    elif (
        index_tip_y < wrist_y
        and middle_tip_y < wrist_y
        and index_tip_y < ring_tip_y
        and index_tip_y < pinky_tip_y
    ):
        cv2.putText(
            image, "Su su!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )
        output = "B"

    elif (
        (ring_tip_y < wrist_y or pinky_tip_y < wrist_y)
        and index_tip_y < wrist_y
        and middle_tip_y < wrist_y
    ):
        cv2.putText(
            image, "None", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )
        output = "C"


while True:
    frame, image = cam.read()
    if not frame:
        print("Your turn off webcam")
        break

    image = cv2.resize(image, (1024, 768))
    image = cv2.flip(image, 1)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=4),  # joints
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=4),  # lines
            )

            wrist_y = 250
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP
            ]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            if thumb_tip and index_tip and middle_tip and ring_tip and pinky_tip:

                thumb_tip_y = thumb_tip.y * image.shape[0]
                index_tip_y = index_tip.y * image.shape[0]
                middle_tip_y = middle_tip.y * image.shape[0]
                ring_tip_y = ring_tip.y * image.shape[0]
                pinky_tip_y = pinky_tip.y * image.shape[0]

                look_a_like(
                    wrist_y,
                    thumb_tip_y,
                    index_tip_y,
                    middle_tip_y,
                    ring_tip_y,
                    pinky_tip_y,
                )

    cv2.imshow("Cam", image)

    if cv2.waitKey(1) & 0xFF == ord("e"):
        break


cam.release()
cv2.destroyAllWindows()
