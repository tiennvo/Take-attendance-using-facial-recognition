import pandas as pd
import queryDB as db
import streamlit as st
import shutil
import os


def export_attendance_records():
    attendance_records = db.getAttendanceRecords()
    if attendance_records:
        df = pd.DataFrame(attendance_records, columns=["ID", "Name", "Check-in", "Check-out"])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Xuất dữ liệu ra CSV",
            data=csv,
            file_name="attendance_records.csv",
            mime="text/csv",
        )

def delete_all_folders(folder_path):
    """
    Xóa tất cả thư mục trong folder_path.
    
    :param folder_path: Đường dẫn đến folder chứa các thư mục cần xóa.
    """
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} không tồn tại.")
        return
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        
        if os.path.isdir(item_path):
            try:
                # Xóa thư mục và tất cả nội dung bên trong
                shutil.rmtree(item_path)
            except Exception as e:
                print(f"Lỗi khi xóa thư mục {item_path}: {e}")