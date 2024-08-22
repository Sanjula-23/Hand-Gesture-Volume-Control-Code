import cv2
import mediapipe as mp
import os
import time

def change_volume(direction):
    try:
        os.system(f"osascript -e 'set volume output volume (output volume of (get volume settings) {direction} 5)'")
    except Exception as e:
        print(f"Error changing volume: {e}")

last_volume_change_time = 0
volume_change_cooldown = 0.5 
dist = 0
x1 = y1 = x2 = y2 = 0

webcam = cv2.VideoCapture(0)
if not webcam.isOpened():
    print("Error: Could not open webcam.")
    exit()

my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

while True:
    _, image = webcam.read()
    image = cv2.flip(image, 1)
    frame_height, frame_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img=image, center=(x, y), radius=14, color=(0, 255, 255), thickness=3)
                    x1 = x
                    y1 = y
                if id == 4:
                    cv2.circle(img=image, center=(x, y), radius=14, color=(0, 0, 255), thickness=3)
                    x2 = x
                    y2 = y
            dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 // 4
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)

        current_time = time.time()
        if current_time - last_volume_change_time > volume_change_cooldown:
            if dist > 50:
                change_volume("+")
                last_volume_change_time = current_time
            elif dist < 30:
                change_volume("-")
                last_volume_change_time = current_time

    cv2.imshow("Hand volume control using python", image)
    key = cv2.waitKey(10)
    if key == 27:
        break

webcam.release()
cv2.destroyAllWindows()
