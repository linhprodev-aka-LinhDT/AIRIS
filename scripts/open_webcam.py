import cv2
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

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

        results = model(frame, conf=0.25, verbose=False)

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label = model.names[class_id]
                if label != "person":
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    label,
                    (x1, max(20, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

        cv2.imshow("AIRIS Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    capture.release()
    cv2.destroyAllWindows()
