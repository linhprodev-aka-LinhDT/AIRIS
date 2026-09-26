import cv2

capture = cv2.VideoCapture(0)
if not capture.isOpened():
    raise RuntimeError("Unable to open webcam source 0")

print("Webcam opened. Press q in the camera window to close.", flush=True)
cv2.namedWindow("AIRIS Webcam", cv2.WINDOW_NORMAL)
cv2.resizeWindow("AIRIS Webcam", 960, 720)

try:
    while True:
        ok, frame = capture.read()
        if not ok:
            raise RuntimeError("Unable to read a frame from webcam source 0")

        cv2.imshow("AIRIS Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    capture.release()
    cv2.destroyAllWindows()
