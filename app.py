from flask import Flask
import pymysql
import os

app = Flask(__name__)

# Nhận thông tin cấu hình DB từ môi trường (do Docker Swarm truyền vào)
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'Dts@1234')
DB_NAME = os.environ.get('DB_NAME', 'lab_db')

def get_db_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)

@app.route('/')
def hello():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Tạo bảng nếu chưa có và thêm 1 lượt truy cập
            cursor.execute('CREATE TABLE IF NOT EXISTS visits (id INT AUTO_INCREMENT PRIMARY KEY, count INT)')
            cursor.execute('INSERT INTO visits (count) VALUES (1)')
            conn.commit()
            
            # Đếm tổng số lượt
            cursor.execute('SELECT COUNT(*) FROM visits')
            total_visits = cursor.fetchone()[0]
        conn.close()
        return f"<h1>Hệ thống Web + MySQL trên Swarm hoạt động mượt mà!</h1><h2>Số lượt truy cập được lưu trong DB: {total_visits}</h2>"
    except Exception as e:
        return f"<h1>Hệ thống đang khởi động kết nối Database...</h1><p>Vui lòng F5 lại sau vài giây (Lỗi: {str(e)})</p>"

if __name__ == "__main__":
    # Chạy ở port 5000
    app.run(host="0.0.0.0", port=5000)
