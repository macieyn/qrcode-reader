# from pyzbar.pyzbar import decode
# from PIL import Image
import numpy as np
import cv2
import datetime
import time
import winsound


frequency = 1500  # Set Frequency To 2500 Hertz
duration = 200  # Set Duration To 1000 ms == 1 second


def square(pts, scale):
    pass


def qr_preview(code, scale):
    height = len(code)
    width = len(code[0])
    img = np.zeros((height * scale, width * scale, 3), np.uint8)
    for (x, row) in enumerate(code):
        for (y, col) in enumerate(row):
            if col == 255:
                cv2.rectangle(
                    img,
                    (x * scale, y * scale),
                    ((x + 1) * scale, (y + 1) * scale),
                    (255, 255, 255),
                    -1,
                )
    return img


cap = cv2.VideoCapture(0)
time.sleep(2)
det = cv2.QRCodeDetector()
color = (0, 255, 0)
detecting = True
detected_at = datetime.datetime.now()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if (
        not detecting
        and detected_at + datetime.timedelta(0, 1) < datetime.datetime.now()
    ):
        detecting = True
    # Detect qr
    if detecting:
        retval, points, straight_qrcode = det.detectAndDecode(frame)
    if retval and detecting:
        winsound.Beep(frequency, duration)
        img = qr_preview(straight_qrcode, 15)
        print(retval)
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        frame = cv2.polylines(frame, [pts], True, color, 2)
        cv2.imshow("qr", img)
        detecting = False
        detected_at = datetime.datetime.now()

    # Display the resulting frame
    cv2.imshow("color", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
