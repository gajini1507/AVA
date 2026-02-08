import cv2
import mediapipe as mp

class VisionEngine:
    def __init__(self):
        # Using the python.solutions path to avoid AttributeErrors
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8
        )
        self.mp_draw = mp.solutions.drawing_utils

    def get_landmarks(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        lm_list = []
        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_lms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
                self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return lm_list

    def get_fingers_up(self, lm_list):
        fingers = []
        # Thumb: Check position relative to joint
        if lm_list[4][1] > lm_list[3][1]: fingers.append(1)
        else: fingers.append(0)
        # 4 Fingers: Check if tip is higher than joint
        for id in [8, 12, 16, 20]:
            if lm_list[id][2] < lm_list[id-2][2]: fingers.append(1)
            else: fingers.append(0)
        return fingers