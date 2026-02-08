import cv2
import pyautogui
import threading
import numpy as np
from vision_module import VisionEngine
from voice_module import VoiceAssistant

# Initialization
vision = VisionEngine()
jarvis = VoiceAssistant()
screen_w, screen_h = pyautogui.size()
keyboard_rows = {1: "QWERTYUIOP", 2: "ASDFGHJKL", 3: "ZXCVBNM"}
active_row = 1

# --- FIXED VOICE THREAD ---
def run_voice():
    jarvis.speak("Stark Systems Online. Ready.")
    while True:
        jarvis.listen_and_execute()

threading.Thread(target=run_voice, daemon=True).start()

# --- CAMERA SETUP ---
cap = cv2.VideoCapture(0)
cap.set(3, 1250) # Width
cap.set(4, 700)  # Height

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    lm_list = vision.get_landmarks(img)

    if lm_list:
        fingers = vision.get_fingers_up(lm_list)
        total_fingers = fingers.count(1)

        # 1. ROW SWAP (Keyboard Logic)
        if 1 <= total_fingers < 4:
            active_row = total_fingers

        #for click
        

        # 2. SMOOTH MOUSE (2 Fingers: Index & Middle)
        if fingers[1] == 1 and fingers[2] == 1 and total_fingers == 2:
            x, y = lm_list[8][1], lm_list[8][2]
            # Mapping from Camera frame to Screen resolution
            sx = np.interp(x, [100, w-100], [0, screen_w])
            sy = np.interp(y, [100, h-100], [0, screen_h])
            pyautogui.moveTo(sx, sy)

        # 3. SCROLLING (0 Fingers = Down | 5 Fingers = Up)
        if total_fingers == 0:
            pyautogui.scroll(-90) # Down
        elif total_fingers == 5:
            pyautogui.scroll(100)  # Up

        # 4. SYSTEM SWIPE (Palm Center height)
        palm_y = lm_list[9][2]
        if palm_y < 150: 
            pyautogui.hotkey('win', 'up') # Maximize
        elif palm_y > h - 150: 
            pyautogui.hotkey('win', 'down') # Minimize

    # HUD Overlay
    cv2.putText(img, f"ACTIVE ROW {active_row}: {keyboard_rows[active_row]}", 
                (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow("Stark OS Interface", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()