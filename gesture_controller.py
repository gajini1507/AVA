import mediapipe as mp # type: ignore


class vision:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

    def fingers(self, hand_landmarks):
        """
        Returns finger state:
        [index, middle, ring, pinky]
        1 = up, 0 = down
        """
        tips = [8, 12, 16, 20]
        fingers = []

        for tip in tips:
            fingers.append(
                hand_landmarks.landmark[tip].y <
                hand_landmarks.landmark[tip - 2].y
            )

        return fingers
