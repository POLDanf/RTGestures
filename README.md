# RTGestures

Real-time hand gesture recognition desktop application built with Python, OpenCV, MediaPipe, and PyQt6.

RTGestures uses your webcam to detect hand landmarks in real time and recognize simple gestures such as:

- ✊ Fist
- ✋ Open Hand
- ✌️ Peace Sign

The application displays live webcam tracking alongside gesture feedback inside a modern PyQt6 interface.

---

## Features

- Real-time webcam hand tracking
- Hand landmark visualization
- Gesture recognition with MediaPipe
- Dual-panel desktop UI using PyQt6
- Supports up to 2 hands simultaneously
- Gesture-triggered actions and image display

---

## Demo

| Gesture | Action |
|---|---|
| FIST | Displays image |
| OPEN HAND | Displays image |
| PEACE | Displays image |

---

## Technologies Used

- Python
- OpenCV
- MediaPipe Tasks API
- PyQt6

---

## Project Structure

```bash
RTGestures/
│
├── main.py
├── hand_landmarker.task
├── Gemini_generated_image_1.png
├── Gemini_generated_image_2.png
├── Gemini_generated_image_3.png
└── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/POLDanf/RTGestures.git

cd RTGestures
```

---

### 2. Create Virtual Environment (Recommended)

#### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install opencv-python mediapipe pyqt6
```

---

## Download the MediaPipe Model

You must download the MediaPipe hand landmark model file:

`hand_landmarker.task`

Place it in the project root directory.

You can download it from the official MediaPipe models page:

https://developers.google.com/mediapipe/solutions/vision/hand_landmarker

---

## Run the Application

```bash
python RTGestures.py
```

---

## How It Works

### Hand Detection

The app uses the MediaPipe Vision Tasks API to:

- Detect hands
- Track landmarks
- Estimate finger positions

---

### Gesture Recognition Logic

Finger states are determined by comparing landmark coordinates.

Example:

```python
finger_is_up(hand_landmarks, 8, 6)
```

Checks whether the index fingertip is above its PIP joint.

The app then classifies gestures based on which fingers are raised.

---

## Current Gestures

### ✊ FIST

All fingers down.

Action:
- Displays an image on the right panel.

---

### ✋ OPEN HAND

All fingers up.

Action:
- Displays an image on the right panel
---

### ✌️ PEACE

Index and middle fingers raised.

Action:
- Displays an image on the right panel

---

## UI Overview

The window contains two panels:

| Panel | Purpose |
|---|---|
| Left | Live webcam feed with landmarks |
| Right | Gesture feedback display |

---

## Future Improvements

Potential enhancements:

- Gesture-controlled media player
- Screenshot automation
- Volume control
- Mouse cursor control
- Custom gesture training
- FPS optimization
- Better thumb detection logic
- Full gesture-action mapping system

---

## Example Requirements File

Create a `requirements.txt`:

```txt
opencv-python
mediapipe
pyqt6
```

---

## Known Limitations

- Thumb detection may vary depending on hand orientation
- Lighting conditions can affect accuracy
- Gesture recognition is currently rule-based
- No GPU acceleration enabled

---

## License

MIT License

Feel free to modify and use this project for learning or personal projects.

---

## Acknowledgements

- MediaPipe — https://developers.google.com/mediapipe
- OpenCV — https://opencv.org/
- PyQt6 Documentation — https://doc.qt.io/qtforpython-6/