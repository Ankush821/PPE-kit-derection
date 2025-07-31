from ultralytics import YOLO
import cv2
import cvzone
import math

def ppe_detection(file=None, mode='with_alert'):
    if file == 0 or file is None:
        cap = cv2.VideoCapture(0)  # Webcam
        cap.set(3, 1280)
        cap.set(4, 720)
    else:
        cap = cv2.VideoCapture(file)

    model = YOLO("best.pt")
    classNames = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest',
                  'Person', 'Safety Cone', 'Safety Vest', 'machinery', 'vehicle']

    while True:
        success, img = cap.read()
        if not success:
            break

        alert = False
        results = model(img, stream=True)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = math.ceil(box.conf[0] * 100) / 100
                cls = int(box.cls[0])
                currentClass = classNames[cls]

                if conf > 0.5:
                    if currentClass in ['NO-Hardhat', 'NO-Safety Vest', 'NO-Mask']:
                        color = (0, 0, 255)  # Red alert color
                        if mode == 'with_alert':
                            alert = True
                    elif currentClass in ['Hardhat', 'Safety Vest', 'Mask']:
                        color = (0, 255, 0)  # Green safe color
                    else:
                        color = (255, 0, 0)  # Other

                    cvzone.putTextRect(img, f'{currentClass} {conf}',
                                       (max(0, x1), max(35, y1)),
                                       scale=1, thickness=1,
                                       colorB=color, colorT=(255, 255, 255),
                                       colorR=color, offset=5)
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)

        yield img, alert

    cap.release()
