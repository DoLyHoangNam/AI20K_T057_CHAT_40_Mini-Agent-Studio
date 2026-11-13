import sqlite3

def upgrade_and_seed_database():
    conn = sqlite3.connect('D:/mini-agent-studio/backend/database.db')
    cursor = conn.cursor()

    # 1. Bổ sung các cột hồ sơ phép năm vào bảng users nếu chưa có
    cursor.execute("PRAGMA table_info(users);")
    columns = [col[1] for col in cursor.fetchall()]

    if 'total_leave_days' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN total_leave_days INTEGER DEFAULT 12;")
    if 'used_leave_days' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN used_leave_days INTEGER DEFAULT 0;")
    if 'tenure_months' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN tenure_months INTEGER DEFAULT 12;")

    # 2. Tạo bảng Quản lý Đơn xin nghỉ phép (leave_requests)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leave_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_name TEXT,
        days_requested INTEGER,
        date_details TEXT,
        status TEXT DEFAULT 'PENDING', -- 'PENDING', 'APPROVED', 'REJECTED'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)

    # 3. Cập nhật dữ liệu chuẩn cho nhân viên Đỗ Lý Hoàng Nam
    cursor.execute("""
    UPDATE users 
    SET tenure_months = 8, total_leave_days = 8, used_leave_days = 2
    WHERE email = 'nam.dlh@vinfast.vn';
    """)

    # Cập nhật cho nhân viên Kế toán Nguyễn Thị Lan
    cursor.execute("""
    UPDATE users 
    SET tenure_months = 72, total_leave_days = 14, used_leave_days = 5
    WHERE email = 'ketoan@vinfast.vn';
    """)

    conn.commit()
    conn.close()
    print("✅ Đã nâng cấp Database: Bảng users có đầy đủ số ngày phép & Bảng leave_requests đã sẵn sàng!")

if __name__ == "__main__":
    upgrade_and_seed_database()
