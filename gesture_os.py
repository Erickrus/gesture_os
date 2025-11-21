import cv2
import mediapipe as mp
import pyautogui
import time
import math
import platform

# --- Device Optimization (M-Series) ---
system_name = platform.system()
is_macos = system_name == "Darwin"

# Use AVFoundation on Mac for hardware accel, otherwise default
if is_macos:
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
else:
    cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

screen_w, screen_h = pyautogui.size()

# --- MediaPipe Setup ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    model_complexity=1, # 1 is accurate/fast enough on M1/M2
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# --- Variables & Tuning ---
cursor_x, cursor_y = 0, 0

# Gesture State
is_pinching = False         # Are fingers physically touching?
drag_active = False         # Is the OS Mouse Button currently down?
pinch_start_time = 0        # When did the pinch start?
pinch_start_pos = (0, 0)    # Where did the pinch start?

# Tuning Constants
PINCH_THRESHOLD = 0.05      # MediaPipe distance unit
CLICK_TIMEOUT = 0.4         # Seconds: fast pinch < 0.4s = Click. > 0.4s = Drag.
DRAG_MOVEMENT_THRESHOLD = 40 # Pixels: If you move this far while pinching, dragging starts immediately.

print("🖐️  Jarvis Smart-Mouse Started.")
print("    - Quick Pinch: Click")
print("    - Pinch + Move: Drag")
print("    - Ctrl+C to Stop")

try:
    while True:
        success, img = cap.read()
        if not success: break

        # Flip & Convert
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Performance tweak: pass by reference, not writeable
        img_rgb.flags.writeable = False
        results = hands.process(img_rgb)
        img_rgb.flags.writeable = True

        if results.multi_hand_landmarks:
            lm = results.multi_hand_landmarks[0].landmark

            # --- 1. Move Cursor ---
            target_x = lm[8].x * screen_w
            target_y = lm[8].y * screen_h
            
            # Smoothing (0.4 is responsive, 0.2 is smoother but laggy)
            cursor_x += (target_x - cursor_x) * 0.4
            cursor_y += (target_y - cursor_y) * 0.4

            # Update real mouse position
            pyautogui.moveTo(cursor_x, cursor_y)

            # --- 2. Gesture Logic ---
            distance = math.hypot(lm[4].x - lm[8].x, lm[4].y - lm[8].y)
            
            # A. PINCH DETECTED
            if distance < PINCH_THRESHOLD:
                if not is_pinching:
                    # >> START NEW PINCH <<
                    is_pinching = True
                    pinch_start_time = time.time()
                    pinch_start_pos = (cursor_x, cursor_y)
                    drag_active = False 
                    # NOTE: We do NOT click mouse down yet!
                
                else:
                    # >> HOLDING PINCH <<
                    # Check if we should transition to "Drag Mode"
                    
                    # 1. Calculate how far we moved since pinch started
                    move_dist = math.hypot(cursor_x - pinch_start_pos[0], cursor_y - pinch_start_pos[1])
                    
                    # 2. Check Time
                    time_held = time.time() - pinch_start_time

                    # Condition to start Dragging:
                    # - Moved significantly (Intentional drag) OR
                    # - Held for a long time (Long press / Intentional hold)
                    if not drag_active and (move_dist > DRAG_MOVEMENT_THRESHOLD or time_held > CLICK_TIMEOUT):
                        pyautogui.mouseDown()
                        drag_active = True
            
            # B. PINCH RELEASED
            else:
                if is_pinching:
                    # >> RELEASED <<
                    is_pinching = False
                    
                    if drag_active:
                        # If we were dragging, just let go
                        pyautogui.mouseUp()
                        drag_active = False
                    else:
                        # If we were NOT dragging yet, it means it was a quick tap without moving much
                        # This is a CLICK
                        pyautogui.click()
                        
except KeyboardInterrupt:
    print("\n🛑 Stopping Jarvis...")
    if drag_active: pyautogui.mouseUp() # Safety release

cap.release()
cv2.destroyAllWindows()
