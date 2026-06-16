from flask import Flask
import pymysql
import os

app = Flask(__name__)

# Nhận thông tin cấu hình DB từ môi trường (do Docker Swarm truyền vào)
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'Dts@1234')
DB_NAME = os.environ.get('DB_NAME', 'lab_db')
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Swarm Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f7fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .hero-section { background: linear-gradient(135deg, #203a43 0%, #2c5364 100%); color: white; padding: 3rem 0; border-radius: 0 0 2rem 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin-bottom: 3rem;}
        .card-custom { border: none; border-radius: 1rem; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.08); transition: transform 0.3s ease; }
        .card-custom:hover { transform: translateY(-5px); }
        .stat-number { font-size: 4rem; font-weight: bold; color: #0d6efd; }
        .server-name { font-size: 2.5rem; font-weight: bold; color: #198754; font-family: monospace; background: #e8f5e9; padding: 10px 20px; border-radius: 10px;}
        .icon-bg { background-color: #e9ecef; width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; font-size: 2.5rem;}
    </style>
</head>
<body>
    <div class="hero-section text-center">
        <div class="container">
            <h1 class="display-5 fw-bold">🚀 Hệ Thống Docker Swarm & MariaDB</h1>
            <p class="lead mt-3">Kiến trúc Load Balancing tự động hóa với CI/CD Pipeline</p>
        </div>
    </div>

    <div class="container">
        <div class="row g-4 justify-content-center">
            <div class="col-md-5">
                <div class="card card-custom h-100 text-center p-4">
                    <div class="icon-bg">📊</div>
                    <h3 class="card-title text-muted mb-4">Lượt Truy Cập (Database)</h3>
                    <div class="card-body d-flex flex-column align-items-center justify-content-center">
                        <span class="stat-number">{{ visits }}</span>
                    </div>
                    <p class="text-muted mt-3 mb-0">Dữ liệu lưu trữ đồng bộ qua Volume</p>
                </div>
            </div>

            <div class="col-md-5">
                <div class="card card-custom h-100 text-center p-4">
                    <div class="icon-bg">🐳</div>
                    <h3 class="card-title text-muted mb-4">Worker Đang Phục Vụ</h3>
                    <div class="card-body d-flex flex-column align-items-center justify-content-center">
                        <span class="server-name">{{ hostname }}</span>
                    </div>
                    <p class="text-danger mt-3 mb-0"><i>Hãy nhấn F5 liên tục để xem Swarm chia tải!</i></p>
                </div>
            </div>
        </div>
        
        <div class="text-center mt-5 mb-4 text-muted">
            <small>Designed for System Administration Lab by Đại</small>
        </div>
    </div>
</body>
</html>
"""
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
