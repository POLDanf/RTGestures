import sys
import cv2
import mediapipe as mp
import time

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QWidget,
    QHBoxLayout,
)

from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt

BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions

HAND_CONNECTIONS = [
    (0,1), (1,2), (2,3), (3,4),
    (0,5), (5,6), (6,7), (7,8),
    (5,9), (9,10), (10,11), (11,12),
    (9,13), (13,14), (14,15), (15,16),
    (13,17), (17,18), (18,19), (19,20),
    (0,17)
]

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2
)

def finger_is_up(hand, tip_id, pip_id):
    return hand[tip_id].y < hand[pip_id].y


def recognize_gesture(hand_landmarks):

    fingers = []

    fingers.append(
        hand_landmarks[4].x < hand_landmarks[3].x
    )

    fingers.append(
        finger_is_up(hand_landmarks, 8, 6)
    )

    fingers.append(
        finger_is_up(hand_landmarks, 12, 10)
    )

    fingers.append(
        finger_is_up(hand_landmarks, 16, 14)
    )

    fingers.append(
        finger_is_up(hand_landmarks, 20, 18)
    )

    total_up = fingers.count(True)

    if total_up == 0:
        return "FIST"

    elif total_up == 5:
        return "OPEN HAND"

    elif fingers[1] and fingers[2]:
        return "PEACE"

    return "UNKNOWN"

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("RTGestures")
        self.showMaximized()

        self.image_label = QLabel()
        self.image_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.image_label.setMinimumSize(640, 480)
        self.image_label.setStyleSheet(
            "background-color: black;"
        )

        self.display_label = QLabel()
        self.display_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.display_label.setMinimumSize(640, 480)
        self.display_label.setStyleSheet(
            "background-color: #222;"
        )

        layout = QHBoxLayout()

        layout.addWidget(self.image_label, 1)
        layout.addWidget(self.display_label, 1)

        layout.setStretch(0, 1)
        layout.setStretch(1, 1)

        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.cap = cv2.VideoCapture(0)

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            1280
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            720
        )

        self.landmarker = HandLandmarker.create_from_options(
            options
        )

        self.gesture_image_P = QPixmap(
            "Gemini_generated_image_1.png"
        )
        self.gesture_image_F = QPixmap(
            "Gemini_generated_image_2.png"
        )
        self.gesture_image_H = QPixmap(
            "Gemini_generated_image_3.png"
        )

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_frame
        )

        self.timer.start(30)

        self.start_time = time.time()

    def update_frame(self):

        ret, frame = self.cap.read()

        if not ret:
            return

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        timestamp = int(
            (time.time() - self.start_time) * 1000
        )

        result = self.landmarker.detect_for_video(
            mp_image,
            timestamp
        )

        h, w, _ = frame.shape

        if result.hand_landmarks:

            for hand_landmarks in result.hand_landmarks:

                points = []

                for lm in hand_landmarks:

                    x = int(lm.x * w)
                    y = int(lm.y * h)

                    points.append((x, y))

                    cv2.circle(
                        frame,
                        (x, y),
                        5,
                        (0, 255, 0),
                        -1
                    )

                for start_idx, end_idx in HAND_CONNECTIONS:

                    cv2.line(
                        frame,
                        points[start_idx],
                        points[end_idx],
                        (255, 0, 0),
                        2
                    )

                gesture = recognize_gesture(
                    hand_landmarks
                )

                cv2.putText(
                    frame,
                    gesture,
                    (
                        points[0][0],
                        points[0][1] - 20
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2
                )

                if gesture == "FIST":

                    scaled_gesture = self.gesture_image_F.scaled(
                        self.display_label.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )

                    self.display_label.setPixmap(
                        scaled_gesture
                    )

                elif gesture == "OPEN HAND":
                    scaled_gesture = self.gesture_image_H.scaled(
                        self.display_label.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )

                    self.display_label.setPixmap(
                        scaled_gesture
                    )

                elif gesture == "PEACE":
                    scaled_gesture = self.gesture_image_P.scaled(
                        self.display_label.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )

                    self.display_label.setPixmap(
                        scaled_gesture
                    )
                else:
                    self.display_label.clear()
                    self.display_label.setText("Do a gesture")
                    self.display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.display_label.clear()
            self.display_label.setText("Do a gesture")
            self.display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        h, w, ch = frame.shape

        bytes_per_line = ch * w

        qt_image = QImage(
            frame.data,
            w,
            h,
            bytes_per_line,
            QImage.Format.Format_RGB888
        )

        webcam_pixmap = QPixmap.fromImage(
            qt_image
        )

        scaled_webcam = webcam_pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.image_label.setPixmap(
            scaled_webcam
        )

    def closeEvent(self, event):

        self.cap.release()

        self.landmarker.close()

        event.accept()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())