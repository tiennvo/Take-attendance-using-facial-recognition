import mysql.connector
import datetime
from tkinter import messagebox
import time

# hàm Connection tới database
def connectdatabase():
    connection=mysql.connector.connect(
        host="localhost",
        database="tiennvoai",
        user="root",
        password=""
    )
    return connection

# hàm insert nếu id nhập vào chưa có trong database và update nếu trong database đã có id
def insertOrUpdate(id,name):
    con=connectdatabase()
    query = "select * from people where id ="+str(id)
    cursor=con.cursor()
    cursor.execute(query)
    records=cursor.fetchall()
    isRecorrdExit = 0
    for row in records:
        isRecorrdExit = 1
    if(isRecorrdExit == 0):
        query = "insert into people (id,name) values (%s,%s)"
        cursor.execute(query,(id,name))
    else:
        query = "update people set name = %s where id = %s" 
        cursor.execute(query,(name,id))
    con.commit()
    con.close()
    cursor.close()

#truy vấn lấy ra tất cả các bản ghi trong bảng people
def getAttendanceRecords():
    conn = connectdatabase()
    cursor = conn.cursor()
    query = """
    SELECT attendance.id, people.Name, attendance.timeCheckIn, attendance.timeCheckOut
    FROM attendance
    JOIN people ON attendance.idPeople = people.Id
    WHERE DATE(attendance.timeCheckIn) = CURDATE()
    AND attendance.timeCheckOut IS NOT NULL
    ORDER BY attendance.timeCheckIn ASC
    """
    cursor.execute(query)
    records = cursor.fetchall()
    conn.close()
    return records

def getFilteredAttendanceRecords(name=None, date=None):
    conn = connectdatabase()
    cursor = conn.cursor()

    if name == "D/s vắng mặt":
        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        query = """
        SELECT p.Id, p.Name, NULL AS timeCheckIn, NULL AS timeCheckOut
        FROM people p
        WHERE p.Id NOT IN (
            SELECT a.idPeople
            FROM attendance a
            WHERE DATE(a.timeCheckIn) = %s
        )
        OR p.Id IN (
            SELECT a.idPeople
            FROM attendance a
            WHERE DATE(a.timeCheckIn) = %s AND a.timeCheckOut IS NULL
        )
        """
        params = [date, date]
    else:
        # Truy vấn mặc định (lấy điểm danh)
        query = """
        SELECT a.id, p.Name, a.timeCheckIn, a.timeCheckOut
        FROM attendance a
        JOIN people p ON a.idPeople = p.Id
        WHERE 1=1
        AND a.timeCheckOut IS NOT NULL
        """
        params = []

        # Lọc theo tên
        if name and name != "All":
            query += " AND p.Name = %s"
            params.append(name)

        # Lọc theo ngày cụ thể
        if date:
            query += " AND DATE(a.timeCheckIn) = %s"
            params.append(date)

    # Sắp xếp (chỉ áp dụng cho truy vấn lấy điểm danh)
    if name != "D/s vắng mặt":
        query += " ORDER BY a.timeCheckIn DESC"
    cursor.execute(query, tuple(params))
    records = cursor.fetchall()
    conn.close()
    return records

# hàm sử lý checkout and checkIn
def checkInAndCheckOut(idPeople):
    check:bool
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur_date = datetime.datetime.now().strftime('%Y-%m-%d')
    con=connectdatabase()
    # truy vấn để lấy ra data     
    query = "select * from attendance where idPeople ="+str(idPeople)+ " and date(timeCheckIn) = '"+cur_date+"'"
    cursor=con.cursor()
    cursor.execute(query)
    records=cursor.fetchall()
    isRecorrdExit = 0
    # nếu câu query trên có dữ liệu thì gán isRecorrExit bằng 1 
    for row in records:
        isRecorrdExit = 1
    # check nếu isRecorrdExit == 0 thì tức là id Người dùng  trong ngày hiện tại chưa có trong database thì mình insert nó vào db
    if(isRecorrdExit == 0):
        query = "insert into attendance (idPeople,timeCheckIn,timeCheckOut) values (%s,%s,%s)"
        cursor.execute(query,(idPeople,cur_time,None))
        check = True
    # nếu isRecorrdExit = 1  thì mình sẽ tính là thời gian checkout
    else:
        query = "update attendance set timeCheckOut = %s where idPeople = %s" 
        cursor.execute(query,(cur_time,idPeople))
        check=False
    con.commit()
    con.close()
    cursor.close()
    return check


# D/s người vắng mặt
def getAbsentPeople():
    conn = connectdatabase()
    cursor = conn.cursor()

    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    query_all_people = "SELECT Id, Name FROM people"
    cursor.execute(query_all_people)
    all_people = cursor.fetchall()
    
    query_attended_people = """
    SELECT DISTINCT idPeople
    FROM attendance
    WHERE DATE(timeCheckIn) = %s
    """
    cursor.execute(query_attended_people, (current_date,))
    attended_people_ids = [row[0] for row in cursor.fetchall()]
    # Tìm những người vắng mặt
    absent_people = [person for person in all_people if person[0] not in attended_people_ids]
    conn.close()
    return absent_people


# hàm tìm kiếm People theeo id
def getProfile(id):
    conn=connectdatabase()
    cmd="select * from people where id = "+str(id)
    cursor=conn.cursor()
    cursor.execute(cmd)
    records=cursor.fetchall()
    profile=None
    for row in records:
        profile=row
    conn.close()
    return profile