import cv2
import mediapipe as mp
import numpy as np
import math
import time
import serial

# ================== Serial ==================
ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)

# ================== حالات ==================
running = False
last_press = 0
PRESS_DELAY = 1.0

# ================== الأزرار ==================
START_BTN = (50, 350, 220, 70)   # x, y, w, h
STOP_BTN  = (370, 350, 220, 70)

# ================== إعدادات ==================
PINCH_THRESHOLD = 35
MIN_DIST = 20
MAX_DIST = 200

# ================== MediaPipe ==================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# ================== دوال ==================
def draw_button(frame, btn, text, color):
    x, y, w, h = btn
    cv2.rectangle(frame, (x, y), (x+w, y+h), color, -1)
    cv2.putText(frame, text, (x+40, y+45),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3)

def inside(btn, x, y):
    bx, by, bw, bh = btn
    return bx < x < bx+bw and by < y < by+bh

# ================== الكاميرا ==================
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]

        thumb = hand.landmark[4]
        index = hand.landmark[8]

        x1, y1 = int(thumb.x * w), int(thumb.y * h)
        x2, y2 = int(index.x * w), int(index.y * h)

        pinch = math.hypot(x2 - x1, y2 - y1)

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
        cv2.circle(frame, (x1,y1), 8, (255,0,255), -1)
        cv2.circle(frame, (x2,y2), 8, (255,0,255), -1)
        cv2.line(frame,(x1,y1),(x2,y2),(255,0,255),3)

        now = time.time()

        # ===== START =====
        if (not running and pinch < PINCH_THRESHOLD and
            inside(START_BTN, x2, y2) and
            now - last_press > PRESS_DELAY):

            running = True
            last_press = now
            print("SYSTEM STARTED")

        # ===== STOP =====
        if (running and pinch < PINCH_THRESHOLD and
            inside(STOP_BTN, x2, y2) and
            now - last_press > PRESS_DELAY):

            running = False
            last_press = now
            ser.write(b"0\n")  # إطفاء الأردوينو
            print("SYSTEM STOPPED")

        # ===== إرسال القيم =====
        if running:
            dist = math.hypot(x2 - x1, y2 - y1)
            value = int(np.interp(dist, [MIN_DIST, MAX_DIST], [0, 255]))
            value = max(0, min(255, value))
            ser.write(f"{value}\n".encode())

            cv2.putText(frame, f"Brigthness: {value} ",
                        (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255,0,0), 2)

    # ===== رسم الأزرار =====
    draw_button(frame, START_BTN, "START", (0,200,0))
    draw_button(frame, STOP_BTN,  "STOP",  (0,0,200))

    status = "RUN..." if running else "STOPPED"
    cv2.putText(frame, f"Status: {status}",
                (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (50,240,240), 2)

    cv2.imshow("Gesture Control with Arduino", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()

