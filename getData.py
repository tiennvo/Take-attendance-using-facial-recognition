import cv2
import numpy as np
import os
import queryDB as db


# nhập id và name người mình muốn add mặt vào
id = input("Nhập Id :")
name = input("Nhập Name :")
# gọi đến hàm insert vào db để lưu trữ thông tin
db.insertOrUpdate(id,name)


# Khởi tạo webcam và đặt độ phân giải của nó thành 1280x720
cam = cv2.VideoCapture(0)
cam.set(3,1280)
cam.set(4,720)

# khởi tạo một đối tượng CascadeClassifier trong thư viện OpenCV với tệp tin XML chứa thông tin về mô hình Cascade để phát hiện khuôn mặt trên hình ảnh đầu vào
detector=cv2.CascadeClassifier("./libs/haarcascade_frontalface_default.xml")





# biến này sẽ được sử dụng để theo dõi số lượng ảnh khuôn mặt được chụp cho người dùng này.
sampleNum=0


while(True):
    # đọc dữ liệu video từ máy ảnh và lưu trữ các khung hình trong biến img.
    ret, img = cam.read()
    # chuyển đổi hình ảnh màu sang độ xám để đơn giản hóa trong việc phát hiện khuôn mặt
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # phát hiện khuôn mặt trong hình ảnh thang độ xám
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        # Vẽ một hình chữ nhật xung quanh khuôn mặt được phát hiện
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        # tạo ra một thư mục có tên dataSet nếu nó chưa tồn tại
        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')
        
        sampleNum=sampleNum+1
        # lưu khuôn mặt được phát hiện vào tệp dataSet
        cv2.imwrite("dataSet/User."+id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('frame',img)
    
    # nhấn phím q để kết thúc chương trình
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # nếu số ảnh lưu được đủ 250 ảnh thì xe dừng chương trình
    elif sampleNum>250:
        break


# giải phóng máy ảnh và phá hủy tất cả các cửa sổ do chương trình tạo ra
cam.release()
cv2.destroyAllWindows()

