import socketio
import face_recognition
import imutils
import pickle
import time
import cv2
import json
import os
import base64

socket = socketio.Client()
socket.connect('http://172.20.10.3:5001')

photo = None


def get_photo(img):
    _, img_encoded = cv2.imencode('.jpg', img)
    # png_as_text = base64.b64encode(img_encoded)
    base64_utf8_str = base64.b64encode(img_encoded).decode('utf-8')
    dataurl = f'data:image/jpg;base64,{base64_utf8_str}'
    return dataurl


cascPathface = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"

faceCascade = cv2.CascadeClassifier(cascPathface)

data = pickle.loads(open('face_enc', "rb").read())

print("Streaming started")

# video_capture = cv2.VideoCapture(0)

video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)


@socket.event
def push_camera():
    try:

        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,
                                             scaleFactor=1.1,
                                             minNeighbors=5,
                                             minSize=(60, 60),
                                             flags=cv2.CASCADE_SCALE_IMAGE)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)
        names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"],
                                                     encoding)
            name = "Незнакомец"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
            names.append(name)
            for ((x, y, w, h), name) in zip(faces, names):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 255, 0), 2)
        # socket.emit("lock_names", names)
        # if len(names) != 0:
        #     for i in names:
        #         if i != "Незнакомец" and i != "":
        #             socket.emit("lock", {"status": 1})
        #             break
        socket.emit('send_photo', {"img": get_photo(frame), "names": names})
    except:
        print("wefweg")
        pass
    print(["хочешь фото не получишь"])
