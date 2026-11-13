import sqlite3

def upgrade_iam_schema():
    conn = sqlite3.connect('D:/mini-agent-studio/backend/database.db')
    cursor = conn.cursor()

    # 1. Thêm tenant_id vào users
    cursor.execute('PRAGMA table_info(users)')
    cols = [c[1] for c in cursor.fetchall()]
    if 'tenant_id' not in cols:
        cursor.execute("ALTER TABLE users ADD COLUMN tenant_id TEXT DEFAULT 'VINFAST'")

    # 2. Thêm tenant_id vào agents
    cursor.execute('PRAGMA table_info(agents)')
    ag_cols = [c[1] for c in cursor.fetchall()]
    if 'tenant_id' not in ag_cols:
        cursor.execute("ALTER TABLE agents ADD COLUMN tenant_id TEXT DEFAULT 'VINFAST'")

    # 3. Thêm tenant_id vào leave_requests
    cursor.execute('PRAGMA table_info(leave_requests)')
    lr_cols = [c[1] for c in cursor.fetchall()]
    if 'tenant_id' not in lr_cols:
        cursor.execute("ALTER TABLE leave_requests ADD COLUMN tenant_id TEXT DEFAULT 'VINFAST'")

    # 4. Tạo tài khoản SUPER_ADMIN toàn quyền nền tảng
    cursor.execute("SELECT COUNT(*) FROM users WHERE email = 'superadmin@platform.vn'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO users (email, hashed_password, full_name, department, role, total_leave_days, used_leave_days, tenure_months, tenant_id)
            VALUES ('superadmin@platform.vn', 'super123', 'Super Admin Nền Tảng (Keycloak/IAM Root)', 'IT_Security', 'SUPER_ADMIN', 30, 0, 99, 'PLATFORM')
        """)

    # 5. Cập nhật tenant_id mặc định
    cursor.execute("UPDATE users SET tenant_id = 'VINFAST' WHERE tenant_id IS NULL OR tenant_id = ''")
    cursor.execute("UPDATE agents SET tenant_id = 'VINFAST' WHERE tenant_id IS NULL OR tenant_id = ''")
    cursor.execute("UPDATE leave_requests SET tenant_id = 'VINFAST' WHERE tenant_id IS NULL OR tenant_id = ''")

    conn.commit()
    conn.close()
    print("✅ CSDL SQLite đã nâng cấp cấu trúc Multi-Tenant IAM và tài khoản SUPER_ADMIN thành công!")

if __name__ == '__main__':
    upgrade_iam_schema()
