import time
import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0
click_active = False
click_threshold = 30
click_duration = 60
last_click_time = 0
middle_finger_y = 0
right_click_active = False
right_click_threshold = 30
right_click_duration = 60
right_last_click_time = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            index_finger = landmarks[8]
            thumb = landmarks[4]
            middle_finger = landmarks[12]
            index_x = int(index_finger.x * frame_width)
            index_y = int(index_finger.y * frame_height)
            thumb_x = int(thumb.x * frame_width)
            thumb_y = int(thumb.y * frame_height)
            middle_x = int(middle_finger.x * frame_width)
            middle_y = int(middle_finger.y * frame_height)
            cv2.circle(img=frame, center=(index_x, index_y), radius=10, color=(0, 255, 255))
            cv2.circle(img=frame, center=(thumb_x, thumb_y), radius=10, color=(0, 255, 255))
            cv2.circle(img=frame, center=(middle_x, middle_y), radius=10, color=(0, 255, 255))
            index_screen_x, index_screen_y = screen_width / frame_width * index_x, screen_height / frame_height * index_y
            pyautogui.moveTo(index_screen_x, index_screen_y)
            if abs(index_y - thumb_y) < click_threshold:
                current_time = time.time()
                if not click_active:
                    pyautogui.mouseDown(button='left')
                    click_active = True
                    last_click_time = current_time
                elif current_time - last_click_time > click_duration:
                    pyautogui.mouseUp(button='left')
                    click_active = False
            else:
                if click_active:
                    pyautogui.mouseUp(button='left')
                    click_active = False

            if abs(index_y - middle_y) < right_click_threshold:
                current_time = time.time()
                if not right_click_active:
                    pyautogui.mouseDown(button='right')
                    right_click_active = True
                    right_last_click_time = current_time
                elif current_time - right_last_click_time > right_click_duration:
                    pyautogui.mouseUp(button='right')
                    right_click_active = False
            else:
                if right_click_active:
                    pyautogui.mouseUp(button='right')
                    right_click_active = False
    else:
        if click_active:
            pyautogui.mouseUp(button='left')
            click_active = False
        if right_click_active:
            pyautogui.mouseUp(button='right')
            right_click_active = False

    cv2.imshow('Hand Gesture Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()