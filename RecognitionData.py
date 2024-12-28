import cv2
import numpy as np
from PIL import Image
import queryDB as db
from time import sleep
from gtts import gTTS
import time
import os

# Khởi tạo webcam và đặt độ phân giải của nó thành 732x720
cam = cv2.VideoCapture(0)
cam.set(3,732)
cam.set(4,720)

# khởi tạo một đối tượng CascadeClassifier trong thư viện OpenCV với tệp tin XML chứa thông tin về mô hình Cascade để phát hiện khuôn mặt trên hình ảnh đầu vào
face_cascade=cv2.CascadeClassifier("libs/haarcascade_frontalface_default.xml")
# tạo ra một đối tượng nhận dạng khuôn mặt bằng thuật toán LBPH
recognizer = cv2.face.LBPHFaceRecognizer_create()
# dùng để đọc dữ liệu được trani từ tệp
recognizer.read('recognizer/trainningData.yml')
imgBackground = cv2.imread('image/background.png')


modeType = 3
last_time_checked = time.time()

fontface = cv2.FONT_HERSHEY_SIMPLEX

folderModePath = 'image'
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

# Vòng lặp vô hạn để lấy liên tục hình ảnh từ camera.
while(True):
    # cam.read() là hàm để đọc hình ảnh từ camera và lưu trữ vào biến frame.
    ret, frame = cam.read()
    # đổi kích thước của hình ảnh.
    frame_resized = cv2.resize(frame, (732, 720))
    imgBackground[0:0+720,0:0+732] = frame_resized
    imgBackground[44:44 + 634,800:800 + 414] = imgModeList[modeType]

    # chuyển đổi hình ảnh màu sang độ xám để đơn giản hóa trong việc phát hiện khuôn mặt
    gray = cv2.cvtColor(imgBackground,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray)
    
    if len(faces) == 0:
        modeType = 3
    else :
        for(x, y, w, h) in faces:
            # Vẽ một hình chữ nhật xung quanh khuôn mặt được phát hiện
            cv2.rectangle(imgBackground,(x , y ),(x + w, y + h),(0,255,0), 2)
            # thực hiện nhận diện khuôn mặt và xác định người đó bằng cách so sánh khuôn mặt được phát hiển từ cam với các khuôn mặt được train trước đó.
            roi_gray = gray[y:y+h, x:x+w]
            # kết quả này trả về là id và confidence -> độ tin cậy
            id,confidence = recognizer.predict(roi_gray)

            if confidence < 100 :
                # gọi đến hàm getProfile để lấy thông tin 
                profile=db.getProfile(id)
                # nếu profile mà không bằng rỗng thì hiển thị tên
                if(profile!=None):
                    # hiển thị ra tên trong khunng cam
                    cv2.putText(imgBackground, "" + str(profile[1]), (x + 10 ,y + h + 30), fontface, 1, (0,255,0),2)
                    cv2.putText(imgBackground, "" + str(100 - round(confidence))+" %", (x + 10 ,y - 10), fontface, 1, (0,255,0),2)
                    current_time = time.time()
                    if (current_time - last_time_checked) >= 3: 
                        # gọi đến hàm checkin
                        check = db.checkInAndCheckOut(profile[0])
                        if check :
                            modeType = 1
                        else:
                            modeType = 2
                        elapsed_time = current_time - last_time_checked
                        last_time_checked = current_time
                        minutes = int(elapsed_time // 60)
                        seconds = elapsed_time % 60
            else :
                cv2.putText(imgBackground, "Unknow:",(x + 10, y + h + 30), fontface, 1, (0,0,255), 2)
                modeType = 4
    
        
    cv2.imshow("Face-Recognition",imgBackground)
    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()