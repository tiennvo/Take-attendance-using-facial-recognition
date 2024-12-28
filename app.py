import streamlit as st
import cv2
import numpy as np
from PIL import Image
import queryDB as db
from time import sleep
from gtts import gTTS
import time
import os
import pandas as pd
import exportdata
import os
import datetime


# Khởi tạo webcam và đặt độ phân giải của nó thành 732x720
cam = cv2.VideoCapture(0)
cam.set(3, 732)
cam.set(4, 720)

# Khởi tạo CascadeClassifier
face_cascade = cv2.CascadeClassifier("libs/haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainningData.yml')
imgBackground = cv2.imread('image/background.png')

modeType = 3
last_time_checked = time.time()
islasttime = True

fontface = cv2.FONT_HERSHEY_SIMPLEX

folderModePath = 'image'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

st.title("Điểm danh bằng khuôn mặt")

image_placeholder = st.empty()

table_placeholder = st.empty()

# Hiển thị dữ liệu check-in và check-out
def show_attendance_records():
    attendance_records = db.getAttendanceRecords()
    if attendance_records:
        df = pd.DataFrame(attendance_records, columns=["ID", "Name", "Check-in", "Check-out"])
        table_placeholder.table(df)
    else:
        table_placeholder.write("No attendance records found.")


def get_user_names():
    conn = db.connectdatabase()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Name FROM people")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names

with st.sidebar:
    st.header("Bộ lọc")
    user_names = get_user_names()
    selected_name = st.selectbox("Tên", ["All"] + ["D/s vắng mặt"] + user_names)
    selected_date = st.date_input("Ngày điểm danh", value=None)

    # Hàm để hiển thị bảng dữ liệu
    def show_attendance(name=None, date=None):
        attendance_records = db.getFilteredAttendanceRecords(name, date)
        if attendance_records:
            df = pd.DataFrame(attendance_records, columns=["ID", "Name", "Check-in", "Check-out"])

            st.table(df)
        else:
            st.write("No attendance records found.")

    # Hiển thị bảng dữ liệu
    name_filter = selected_name if selected_name != "All" else None
    date_filter = selected_date.strftime('%Y-%m-%d') if selected_date else None
    show_attendance(name_filter, date_filter)

    exportdata.export_attendance_records()


show_attendance_records()

exportdata.delete_all_folders('log')

while True:
    ret, frame = cam.read()
    frame_resized = cv2.resize(frame, (732, 720))
    imgBackground[0:0+720, 0:0+732] = frame_resized
    imgBackground[44:44 + 634, 800:800 + 414] = imgModeList[modeType]

    gray = cv2.cvtColor(imgBackground, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    if len(faces) == 0:
        modeType = 3
    else:
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            id, confidence = recognizer.predict(roi_gray)

            if confidence < 80:
                profile = db.getProfile(id)
                if profile is not None:
                    cv2.rectangle(imgBackground, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(imgBackground, "" + str(profile[1]), (x + 10, y + h + 30), fontface, 1, (0, 255, 0), 2)
                    cv2.putText(imgBackground, "" + str(100 - round(confidence)) + " %", (x + 10, y - 10), fontface, 1, (0, 255, 0), 2)
                    current_time = time.time()
                    if islasttime:
                        last_time_checked = current_time
                        islasttime = False
                    if (current_time - last_time_checked) >= 5:
                        path = 'log/' + str(profile[1])
                        filename = path + '/' + str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')) + '.jpg'
                        if not os.path.exists(path):
                            os.makedirs(path)
                        cv2.imwrite(filename, frame_resized)
                        check = db.checkInAndCheckOut(profile[0])
                        if check:
                            modeType = 1
                        else:
                            modeType = 2

                        show_attendance_records()
                        islasttime = True
                        elapsed_time = current_time - last_time_checked
                        last_time_checked = current_time
                        minutes = int(elapsed_time // 60)
                        seconds = elapsed_time % 60
            else:
                cv2.rectangle(imgBackground, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(imgBackground, "Unknow:", (x + 10, y + h + 30), fontface, 1, (0, 0, 255), 2)
                modeType = 4
    image_placeholder.image(imgBackground, channels="BGR")

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()