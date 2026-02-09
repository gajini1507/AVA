import cv2 # type: ignore
import pyautogui  # type: ignore
import threading
import time
from gesture_controller import vision
from voice_assistant import AVA
from ui import AVA_UI

# ================== CONSTANTS ==================
COOLDOWN = 1.5
SCREEN_W, SCREEN_H = pyautogui.size()

mouse_mode = False
def set_mouse_mode(value: bool):
    global mouse_mode
    mouse_mode = value

def get_mouse_mode() -> bool:
    return mouse_mode

# ================== OBJECTS ==================
v = vision()
ava = AVA()
ui = AVA_UI()

last_action_time = 0
voice_thread = None


# ================== VOICE THREAD ==================
def run_voice():
    print("waiting for wake...")
    while True:
        ui.update("Voice Mode 🎤", "#00ccff")
        ava.run()

# ================== GESTURE THREAD ==================
def run_gesture():
    global last_action_time, voice_thread

    cap = cv2.VideoCapture(0)
    ui.update("Gesture System Ready")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = v.hands.process(rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            v.mp_draw.draw_landmarks(frame, hand, v.mp_hands.HAND_CONNECTIONS)

            fingers = v.fingers(hand)
            now = time.time()

            # ========== MOUSE MODE ==========
            if get_mouse_mode():
                ui.update(
                "Mouse Mode ON 🖱" if get_mouse_mode else "Gesture Mode ✋",
                "#00ff00" if mouse_mode else "#ff5555" )
                last_action_time = now

                if fingers == [1, 1, 0, 0]:
                    x = int(hand.landmark[9].x * SCREEN_W)
                    y = int(hand.landmark[9].y * SCREEN_H)
                    pyautogui.moveTo(x, y, duration=0.05)

                elif fingers == [0, 0, 0, 0]:
                    pyautogui.click()
                    time.sleep(0.3)

            # ========== GESTURE MODE ==========
            else:
                if now - last_action_time > COOLDOWN:

                    # ✊ SCROLL DOWN
                    if fingers == [0, 0, 0, 0] and mouse_mode == False:
                        pyautogui.scroll(-300)
                        last_action_time = now

                    # ✋ SCROLL UP
                    elif fingers == [1, 1, 1, 1]:
                        pyautogui.scroll(300)
                        last_action_time = now

                    #☝VOICE
                    elif fingers == [1,0,0,0]:
                        if voice_thread is None or not voice_thread.is_alive():
                            voice_thread = threading.Thread(
                                target=run_voice, daemon=True
                            )
                            voice_thread.start()
                            last_action_time = now

                    # ✌ MINIMIZE
                    elif fingers == [1, 1, 0, 0] and mouse_mode == False:
                        pyautogui.hotkey("win", "down")
                        last_action_time = now

                    # 🤟 MAXIMIZE
                    elif fingers == [1, 1, 1, 0] and mouse_mode == False:
                        pyautogui.hotkey("win", "up")
                        last_action_time = now

        # Overlay
        mode_text = "MOUSE MODE" if mouse_mode else "GESTURE MODE"
        cv2.putText(frame, mode_text, (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2)

        cv2.imshow("AVA – Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# ================== MAIN ==================
if __name__ == "__main__":

    # Start gesture in background
    threading.Thread(target=run_gesture, daemon=True).start()

    # UI MUST run in main thread
    ui.start()
