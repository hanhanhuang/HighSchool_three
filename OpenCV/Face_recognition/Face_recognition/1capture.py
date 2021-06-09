import cv2
ESC = 27
# 畫面(幀)數量計數
n = 1
# 存檔檔名用
index = 0
# 人臉取樣總數
total = 200

def saveImage(face_image, index):
    filename = 'images/h0/{:02d}.pgm'.format(index)
    cv2.imwrite(filename, face_image)
    print(filename)
    
# 告訴OpenCV使用人臉識別分類器
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 視訊來源
cap = cv2.VideoCapture(0)

cv2.namedWindow('video', cv2.WINDOW_NORMAL)

while n > 0:
    ret, frame = cap.read() #讀取一幀資料
    # frame = cv2.resize(frame, (600, 336))
    frame = cv2.flip(frame, 1)
    
    # 將當前幀轉換成灰度影象
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#### 在while內
    faces = face_cascade.detectMultiScale(gray, 1.1, 8)
    # .detectMultiScale(灰度圖檔, scaleFactor, minNeighbors)
    # scaleFactor影象縮放比例，可以理解為同一個物體與相機距離不同，其大小亦不同，必須將其縮放到一定大小才方便識別，該引數指定每次縮放的比例
    # minNeighbors：對特徵檢測點周邊多少有效點同時檢測，這樣可避免因選取的特徵檢測點太小而導致遺漏

    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if n % 2 == 0: # 每兩幀存一次
            face_image = cv2.resize(gray[y: y + h, x: x + w], (400, 400))
            
            # 將當前幀儲存為圖片
            saveImage(face_image, index)
            index += 1
            if index >= total:  # 如果超過指定最大儲存數量退出迴圈
                print('get training data done')                
                n = -1
                break
        
        # 顯示當前捕捉到了多少人臉圖片
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'num:%d' % (index),(x + 30, y + 30), font, 1, (255,0,255),4)  
        
        n += 1 # 計數幀數

#### 在while內
    # 顯示影象
    cv2.imshow('video', frame)
    if cv2.waitKey(1) == 27 or index>=total: # 如果超過指定最大儲存數量關閉程式
        #銷燬所有視窗
        cv2.destroyAllWindows()
        break