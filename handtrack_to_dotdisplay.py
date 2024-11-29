import mediapipe as mp
import cv2
import serial
import time

cv2.VideoCapture(0)
cam = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
# USB-to-serial
nano = serial.Serial("COM3", 115200)


data_landmark = {}
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


def Normalized(image, hand_landmarks):
    # Normalized pixel
    image_height = image.shape[0]  # y-axis
    image_width = image.shape[1]  # x-axis
    for landmarks in mp_hands.HandLandmark:
        if landmarks in my_landmarks:
            x = hand_landmarks.landmark[landmarks].x * image_width
            y = hand_landmarks.landmark[landmarks].y * image_height
            data_landmark[landmarks.name] = {"X": x, "Y": y}
    # print("Chech Data:", data_landmark)
    # time.sleep(1)
    return data_landmark


def process(data_landmark, image):
    wrist_x = data_landmark["WRIST"]["X"]
    wrist_y = data_landmark["WRIST"]["Y"]
    thumb_mcp_x = data_landmark["THUMB_MCP"]["X"]
    thumb_mcp_y = data_landmark["THUMB_MCP"]["Y"]
    thumb_tip_x = data_landmark["THUMB_TIP"]["X"]
    thumb_tip_y = data_landmark["THUMB_TIP"]["Y"]
    index_finger_pip_x = data_landmark["INDEX_FINGER_PIP"]["X"]
    index_finger_pip_y = data_landmark["INDEX_FINGER_PIP"]["Y"]
    index_finger_tip_x = data_landmark["INDEX_FINGER_TIP"]["X"]
    index_finger_tip_y = data_landmark["INDEX_FINGER_TIP"]["Y"]
    middle_finger_pip_x = data_landmark["MIDDLE_FINGER_PIP"]["X"]
    middle_finger_pip_y = data_landmark["MIDDLE_FINGER_PIP"]["Y"]
    middle_finger_tip_x = data_landmark["MIDDLE_FINGER_TIP"]["X"]
    middle_finger_tip_y = data_landmark["MIDDLE_FINGER_TIP"]["Y"]
    ring_finger_pip_x = data_landmark["RING_FINGER_PIP"]["X"]
    ring_finger_pip_y = data_landmark["RING_FINGER_PIP"]["Y"]
    ring_finger_tip_x = data_landmark["RING_FINGER_TIP"]["X"]
    ring_finger_tip_y = data_landmark["RING_FINGER_TIP"]["Y"]
    pinky_pip_x = data_landmark["PINKY_PIP"]["X"]
    pinky_pip_y = data_landmark["PINKY_PIP"]["Y"]
    pinky_tip_x = data_landmark["PINKY_TIP"]["X"]
    pinky_tip_y = data_landmark["PINKY_TIP"]["Y"]

    # goodjob
    if (
        wrist_x > thumb_mcp_x > thumb_tip_x > index_finger_tip_x > index_finger_pip_x
    ) and (pinky_pip_y > wrist_y > ring_finger_tip_y > thumb_mcp_y > thumb_tip_y):
        print("goodjob")
        cv2.putText(
            image, "Goodjob", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 4
        )
        nano.write(bytes("A", "utf-8"))

    # fighting
    if (
        pinky_pip_x > middle_finger_tip_x > ring_finger_tip_x > index_finger_pip_x
    ) and (
        wrist_y > thumb_mcp_y > pinky_pip_y > ring_finger_pip_y > middle_finger_pip_y
    ):
        print("fighting")
        cv2.putText(
            image, "Fighting", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 4
        )
        nano.write(bytes("B", "utf-8"))

    # love
    if (pinky_pip_x > ring_finger_tip_x > middle_finger_tip_x > thumb_tip_x) and (
        wrist_y
        > thumb_mcp_y
        > middle_finger_tip_y
        > thumb_tip_y
        > pinky_pip_y
        > pinky_tip_y
    ):
        print("love")
        cv2.putText(image, "love", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 4)
        nano.write(bytes("C", "utf-8"))

    # star
    if (
        pinky_tip_x
        > ring_finger_tip_x
        > wrist_x
        > index_finger_tip_x
        > thumb_mcp_x
        > thumb_tip_x
    ) and (
        wrist_y
        > thumb_mcp_y
        > thumb_tip_y
        > pinky_pip_y
        > ring_finger_pip_y
        > index_finger_tip_y
    ):
        print("star")
        cv2.putText(
            image, "star", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 4
        )
        nano.write(bytes("D", "utf-8"))


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
        Normalized(image, hand_landmarks)
        process(data_landmark, image)
    cv2.imshow("Cam", image)

    # Exit Program
    if cv2.waitKey(1) == ord("e"):
        break


cam.release()
cv2.destroyAllWindows()
