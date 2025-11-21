# 🖐️ GestureOS
### The Future is in Your Hands.

**Forget the mouse. Forget the trackpad.**
GestureOS transforms your standard webcam into a high-precision, AI-powered input device. Built on computer vision, it lets you control your computer with nothing but the air.

Whether you are on a Mac or a standard PC, GestureOS provides a "Minority Report" style interface that feels magical, responsive, and surprisingly practical.

---

## 🚀 Features

*   **👆 Precision Tracking:** Uses Google MediaPipe to track your index fingertip with sub-millimeter precision.
*   **🧠 Smart Click Engine:** Intelligently distinguishes between a **Tap** (Click) and a **Grab** (Drag) using a state-machine logic. No more accidental drags!
*   **🍎 Apple Silicon Optimized:** Automatically detects macOS M-Series chips and forces hardware-accelerated `AVFoundation` capture for blazing-fast performance.
*   **👻 Invisible Mode:** Runs in the background without cluttering your screen with camera windows.

---

## 📦 Installation

### 1. Prerequisites
You need **Python 3.8** or higher installed on your system.

### 2. Install Dependencies
Open your terminal or command prompt and install the required libraries:

```bash
pip install opencv-python mediapipe pyautogui
```

### 3. Get the Code
Save your script code into a file named `gesture_os.py`.

---

## 🍎 macOS Setup Guide (Important!)
**Read this if you are on a Mac.** macOS has strict security protocols that block software from controlling the mouse unless explicitly allowed.

### 1. Grant Accessibility Permissions
For GestureOS to move your cursor, you must grant "Accessibility" access to the terminal or IDE you are running it from.

1.  Open **System Settings** (or System Preferences).
2.  Go to **Privacy & Security** > **Accessibility**.
3.  Click the **+** (plus) button (you may need to enter your password).
4.  Add the application you are using to run the script:
    *   If running from **VS Code**, add Visual Studio Code.
    *   If running from **Terminal**, add Terminal (or iTerm).
    *   If running from **PyCharm**, add PyCharm.
5.  **Restart** your terminal/IDE for the changes to take effect.

### 2. Run the Script
```bash
python3 gesture_os.py
```

---

## 🎮 How to Use

Once the script is running, lift your hand in front of the camera.

### 📍 The Cursor
*   **Pose:** Point your **Index Finger** up.
*   **Action:** The mouse cursor will follow the tip of your index finger.
*   **Tip:** Keep your hand about 1-2 feet away from the camera for the best range of motion.

### 🖱️ The Gestures (Smart Logic)

GestureOS uses a "Smart Logic" buffer to tell the difference between clicking and dragging.

| Action | Gesture | How it works |
| :--- | :--- | :--- |
| **Left Click** | **The "Snap"**<br>Pinch your Thumb and Index finger together and release quickly. | If you pinch and release in less than **0.4 seconds** without moving much, it triggers a click. |
| **Drag & Drop** | **The "Grab"**<br>Pinch your Thumb and Index finger and **Hold**. | If you hold the pinch longer than **0.4s** OR if you pinch and immediately move your hand, the system engages "Drag Mode" (Mouse Down). |
| **Release Drag** | **Open Hand**<br>Release the pinch. | Simply separate your fingers to drop the item (Mouse Up). |

---

## ⚠️ Troubleshooting & Safety

**1. Emergency Stop**
If the mouse starts acting crazy (e.g., bad lighting causing false positives), you have two safety mechanisms:
*   **Ctrl + C:** Click inside your terminal window and press `Ctrl+C` to kill the process.
*   **The Corner Failsafe:** Slam your physical mouse (or the gesture cursor) into any of the **four corners** of the screen. `PyAutoGUI` is configured to crash the script immediately as a safety measure.

**2. Jittery Cursor?**
Ensure your room is well-lit. Dark rooms make it hard for the camera to see the tip of your finger clearly.

**3. "AttributeError: module 'cv2' has no attribute 'CAP_AVFOUNDATION'"**
If you see this on Windows/Linux, don't worry. The script automatically handles this, but ensure you are running the latest version of OpenCV (`pip install --upgrade opencv-python`).

---

## 📝 License
Feel free to modify, distribute, and use GestureOS for your own sci-fi projects!

**Now, put down the mouse and wave at your screen. 👋**
