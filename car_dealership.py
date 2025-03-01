import mysql.connector

# Kết nối tới MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",  # Địa chỉ MySQL Server
        user="root",       # Tên người dùng MySQL
        password="tramdac10092004",       # Mật khẩu MySQL (để trống nếu không có)
        database="CarDealership"  # Tên cơ sở dữ liệu
    )

# Hàm thực thi câu lệnh SQL (SELECT)
def fetch_data(query, params=None):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    conn.close()
    return result

# Hàm thực thi câu lệnh SQL (INSERT, UPDATE, DELETE)
def execute_query(query, params=None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    conn.close()
