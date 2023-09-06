from imutils import paths
import face_recognition
import pickle
import cv2
import os

# получить путь к каждому файлу в папке IMAGES
# Изображения здесь  данные (папки разных лиц)
# создаем списки: 1.прописываем путь к изображению
# Нам также нужно инициализировать два списка до начала цикла, knownEncodings и knownNames.
# Эти два списка содержат данные кодировки лица и имена соответствующих символов в наборе данных
imagePaths = list(paths.list_images('Images'))
knownEncodings = []
knownNames = []
# цикл который обрабатывает лица в наборе данных
for (i, imagePath) in enumerate(imagePaths):
    # извлекаю имя пользователя из пути к изображению
    name = imagePath.split(os.path.sep)[-2]
    # загружаю входное изображение и преобразую его из BGR 
    # для упорядочения dlib в RGB
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Использую Face_recognition для определения местоположения лиц.
    boxes = face_recognition.face_locations(rgb, model='hog')
    # вычисляем встраивание лица для лица
    encodings = face_recognition.face_encodings(rgb, boxes)
    # перебирайте кодировки в цикле
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)
# сохраняйте emcodings вместе с их названиями в данных словаря
data = {"encodings": knownEncodings, "names": knownNames}
# сохраняем данные в файл для последующего использования
f = open("face_enc", "wb")
f.write(pickle.dumps(data))
f.close()
