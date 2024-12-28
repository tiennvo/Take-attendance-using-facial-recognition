import cv2
import os
import numpy as np
from PIL import Image

# tạo ra một đối tượng nhận dạng khuôn mặt bằng thuật toán LBPH
recognizer = cv2.face.LBPHFaceRecognizer_create()
#  đường dẫn đến thư mục chứa hình ảnh khuôn mặt.
path='dataSet'

# Hàm này đọc các hình ảnh khuôn mặt từ thư mục
# hàm này trả về Id Của người trong ảnh và hình ảnh tương ứng
def getImagesAndLabels(path):
    # sử dụng mô-đun os để lấy danh sách tất cả các tệp hình ảnh trong thư mục rồi lặp qua từng tệp để đọc dữ liệu hình ảnh
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        faceImg=Image.open(imagePath).convert('L')
        faceNp=np.array(faceImg,'uint8')
        ID=int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
        cv2.waitKey(1)
    return IDs, faces



# Hàm này gọi hàm getImagesAndLabelshàm lấy IDs và faces 
def trainData():
    Ids,faces=getImagesAndLabels(path)
    # sử dụng phương thức train của recognizer
    recognizer.train(faces,np.array(Ids))
    # lưu vào tệp trainningData.yml
    recognizer.save('recognizer/trainningData.yml')
    print('train success')

trainData()
cv2.destroyAllWindows()
