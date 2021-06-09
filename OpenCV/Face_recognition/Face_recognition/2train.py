import cv2
import numpy as np

images = []
labels = []
for index in range(200):
    filename = 'images/h0/{:02d}.pgm'.format(index)
    print('read ' + filename)
    img = cv2.imread(filename, cv2.COLOR_BGR2GRAY)
    images.append(img)
    labels.append(0)    # 第一位人臉的標籤為0

print('training...')
model = cv2.face.LBPHFaceRecognizer_create()
model.train(np.asarray(images), np.asarray(labels))
model.save('faces.data')
print('training done')
