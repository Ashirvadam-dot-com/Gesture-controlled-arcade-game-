# Hand Gesture Detection — MediaPipe & OpenCV

Real-time hand gesture recognition from a live webcam feed using Python, OpenCV, and MediaPipe.

---

## 📁 Project Structure

```
├── submission.py               # Task submission — single hand gesture detection
├── main.py                     # Personal extension — dual-hand tracking
├── Gestures.py                 # Modular gesture classification (both hands)
├── mediapipe_setup.py          # MediaPipe setup & landmark utilities
└── pinichDurationANDfiring.py  # Timed gesture events (pinch hold & fire combo)
```

---

## 📌 Week 3 & 4 — Task (`submission.py`)

The assigned task was to build a gesture detection system for a **single hand** using MediaPipe landmarks. The program detects the hand from a live webcam feed, classifies the gesture in real time, and displays the label on screen.

Gesture classification works by checking the state of each finger — whether its tip landmark is above or below its base joint — and mapping that combination to a gesture label. Pinch is detected by measuring the pixel distance between the thumb tip and index fingertip.

---

## 💡 Personal Extension (`main.py`)

Going beyond the task, `main.py` extends the system to track **both hands simultaneously**. Each hand is independently classified and displayed on its own side of the screen (left / right), with a live FPS counter.

The key improvement here is the use of **normalized distance** for pinch detection instead of a raw pixel threshold. The distance between the thumb and index finger is divided by the palm size (wrist to middle finger base), making it consistent regardless of how close or far the hand is from the camera.

Additional files `Gestures.py` and `mediapipe_setup.py` were written to keep the logic modular and reusable, and `pinichDurationANDfiring.py` adds a timed event layer — a pinch held for 3+ seconds registers as a `GRAB`, and a `POINTING` right hand combined with a `FIST` left hand triggers a `FIRE` event.

---

## 🖐️ Gestures Supported

| Gesture | Trigger |
|---|---|
| `FIST` | All fingers closed |
| `OPEN PALM` | All fingers open |
| `POINTING` | Index finger only |
| `PEACE` | Index + middle finger |
| `PINCH` | Thumb & index close together |
| `GRAB` | Pinch held for 3+ seconds |
| `FIRE` | Right hand POINTING + Left hand FIST |

---

## 🛠️ Requirements

```bash
pip install opencv-python mediapipe
```

## ▶️ Usage

```bash
python submission.py   # week 3 & 4 task
python main.py         # extended dual-hand version
```
Press `Q` to quit.
