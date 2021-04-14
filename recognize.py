import numpy as np
import imutils
import pickle
import time
import cv2
import markAttendance

def recognizeStudent():
    embeddingFile = "output/embeddings.pickle"
    embeddingModel = "nn4.small2.v1.t7"
    recognizerFile = "output/recognizer.pickle"
    labelEncFile = "output/le.pickle"
    conf = 0.5

    print("[INFO] loading face detector...")
    prototxt = "model/deploy.prototxt"
    model = "model/res10_300x300_ssd_iter_140000.caffemodel"
    detector = cv2.dnn.readNetFromCaffe(prototxt, model)

    print("[INFO] loading face recognizer...")
    embedder = cv2.dnn.readNetFromTorch(embeddingModel)

    recognizer = pickle.loads(open(recognizerFile, "rb").read())
    le = pickle.loads(open(labelEncFile, "rb").read())

    Roll_Number = ""
    box = []
    print("[INFO] starting video stream...")
    cam = cv2.VideoCapture(0)
    time.sleep(2.0)
    tName = ''
    flag = True

    while True:
        _, frame = cam.read()
        frame = imutils.resize(frame, width=600)
        (h, w) = frame.shape[:2]
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)

        detector.setInput(imageBlob)
        detections = detector.forward()

        for i in range(0, detections.shape[2]):

            confidence = detections[0, 0, i, 2]

            if confidence > conf:

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                face = frame[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                if fW < 20 or fH < 20:
                    continue

                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
                embedder.setInput(faceBlob)
                vec = embedder.forward()

                preds = recognizer.predict_proba(vec)[0]
                j = np.argmax(preds)
                proba = preds[j]
                name = le.classes_[j]

                if flag:
                    tName = name

                if tName != name:
                    flag = True
                    tName = name

                if tName == name and flag:
                    markAttendance.fetchData(name)
                    flag = False

                text = "{} : {} : {:.2f}%".format(name, Roll_Number, proba * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              (0, 0, 255), 2)
                cv2.putText(frame, text, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
