import cv2
import face_recognition
import os

cap = cv2.VideoCapture(0)

#получаем изображение
image_to_recognition = face_recognition.load_image_file('litso.jpg') 

#получаем "код" лица
img_code = face_recognition.face_encodings(image_to_recognition)[0]

#Загрузка обученной модели распознавания лиц 
recognizer_cc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#вывод изображения
while True:
    success,img = cap.read()
    #поиск лица
    recognize = recognizer_cc.detectMultiScale(img, scaleFactor=2, minNeighbors=3)
    #Если на видео есть лицо
    if len(recognize) != 0:
        print("Обнаружено лицо")
        #Кодируем неизвестное лицо
        unknown_face = face_recognition.face_encodings(img)
        #сравниваем неизвестное лицо с сохраненным
        compare = face_recognition.compare_faces([unknown_face], img_code)
    if compare == True:
        #Если мы зашли сюда, значит лица одинаковые
        print('Свой, проходи')
    else:
        print('Доступ запрещен')
