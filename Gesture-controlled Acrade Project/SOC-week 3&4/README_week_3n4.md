Hand Gesture Detection — MediaPipe & OpenCV<br>

Real-time hand gesture recognition from a live webcam feed using Python, OpenCV, and MediaPipe.<br>


---

## 📁 Project Structure

```
├── submission.py               # Task submission — single hand gesture detection
├── main.py                     # Extended version with dual-hand tracking & FPS display
├── Gestures.py                 # Modular gesture classification (both hands)
├── mediapipe_setup.py          # MediaPipe setup & landmark utilities
└── pinichDurationANDfiring.py  # Timed gesture events (pinch hold & fire combo)
```

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

---

Press `Q` to quit.
