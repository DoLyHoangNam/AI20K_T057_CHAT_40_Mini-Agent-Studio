import sqlite3

def init_clean_saas_db():
    conn = sqlite3.connect('D:/mini-agent-studio/backend/database.db')
    cursor = conn.cursor()

    # Xóa sạch cấu trúc cũ để dựng kiến trúc chuẩn SaaS Multi-Tenant chuyên nghiệp
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS tenants")
    cursor.execute("DROP TABLE IF EXISTS agents")
    cursor.execute("DROP TABLE IF EXISTS leave_requests")

    # 1. BẢNG DOANH NGHIỆP MUA BẢN QUYỀN (TENANTS)
    cursor.execute("""
        CREATE TABLE tenants (
            id TEXT PRIMARY KEY,               -- 'VINFAST', 'FPT', 'VIETTEL'
            name TEXT NOT NULL,                -- 'Tập đoàn VinFast'
            contact_email TEXT NOT NULL,
            plan_type TEXT DEFAULT 'ENTERPRISE', -- 'TRIAL', 'PROFESSIONAL', 'ENTERPRISE'
            max_agents INTEGER DEFAULT 10,
            max_employees INTEGER DEFAULT 500,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. BẢNG TÀI KHOẢN NGƯỜI DÙNG (USERS)
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id TEXT NOT NULL,          -- 'PLATFORM' (cho SuperAdmin) hoặc mã công ty
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            department TEXT NOT NULL,         -- 'HR', 'Marketing', 'Accounting', 'Production', 'Engineering'
            role TEXT NOT NULL,               -- 'SUPER_ADMIN', 'TENANT_ADMIN', 'EMPLOYEE'
            tenure_months INTEGER DEFAULT 12,
            total_leave_days INTEGER DEFAULT 12,
            used_leave_days INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
    """)

    # 3. BẢNG AI AGENTS (AGENTS)
    cursor.execute("""
        CREATE TABLE agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id TEXT NOT NULL,          -- Thuộc doanh nghiệp nào
            name TEXT NOT NULL,
            description TEXT,
            instruction TEXT NOT NULL,        -- System Prompt
            department_access TEXT DEFAULT 'ALL', -- 'ALL' hoặc phòng ban cụ thể
            is_published INTEGER DEFAULT 1,
            creator_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
    """)

    # 4. BẢNG ĐƠN XIN NGHỈ PHÉP (LEAVE_REQUESTS)
    cursor.execute("""
        CREATE TABLE leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            days_requested INTEGER NOT NULL,
            date_details TEXT NOT NULL,
            status TEXT DEFAULT 'PENDING',    -- 'PENDING', 'APPROVED', 'REJECTED'
            notified_to_user INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # ------------------ SEED DỮ LIỆU CHUẨN MẪU BAN ĐẦU ------------------

    # Cấp 1: Doanh nghiệp
    cursor.execute("INSERT INTO tenants (id, name, contact_email, plan_type) VALUES ('PLATFORM', 'Mini Agent Studio Platform', 'superadmin@platform.vn', 'UNLIMITED')")
    cursor.execute("INSERT INTO tenants (id, name, contact_email, plan_type) VALUES ('VINFAST', 'Tập đoàn VinFast', 'admin@vinfast.vn', 'ENTERPRISE')")
    cursor.execute("INSERT INTO tenants (id, name, contact_email, plan_type) VALUES ('FPT', 'Tập đoàn FPT', 'admin@fpt.vn', 'ENTERPRISE')")

    # Cấp 2: Người dùng
    # 1. DUY NHẤT 1 TÀI KHOẢN SUPER ADMIN CỦA BẠN (CHỦ NỀN TẢNG)
    cursor.execute("""
        INSERT INTO users (tenant_id, email, hashed_password, full_name, department, role, total_leave_days, used_leave_days, tenure_months)
        VALUES ('PLATFORM', 'superadmin@platform.vn', 'super123', 'Super Admin (Chủ Nền Tảng)', 'Executive', 'SUPER_ADMIN', 30, 0, 99)
    """)

    # 2. TÀI KHOẢN ADMIN VINFAST (DO SUPER ADMIN CẤP KHI MUA)
    cursor.execute("""
        INSERT INTO users (tenant_id, email, hashed_password, full_name, department, role, total_leave_days, used_leave_days, tenure_months)
        VALUES ('VINFAST', 'admin@vinfast.vn', 'admin123', 'Quản Trị Viên Nhân Sự VinFast', 'HR', 'TENANT_ADMIN', 14, 0, 24)
    """)

    # 3. NHÂN VIÊN CỦA VINFAST
    cursor.execute("""
        INSERT INTO users (tenant_id, email, hashed_password, full_name, department, role, total_leave_days, used_leave_days, tenure_months)
        VALUES ('VINFAST', 'nam.dlh@vinfast.vn', '123456', 'Đỗ Lý Hoàng Nam', 'Production', 'EMPLOYEE', 8, 2, 8)
    """)
    cursor.execute("""
        INSERT INTO users (tenant_id, email, hashed_password, full_name, department, role, total_leave_days, used_leave_days, tenure_months)
        VALUES ('VINFAST', 'mai.tt@vinfast.vn', '123456', 'Trần Thị Mai', 'Marketing', 'EMPLOYEE', 12, 1, 12)
    """)

    # 4. TÀI KHOẢN ADMIN FPT (DO SUPER ADMIN CẤP KHI MUA)
    cursor.execute("""
        INSERT INTO users (tenant_id, email, hashed_password, full_name, department, role, total_leave_days, used_leave_days, tenure_months)
        VALUES ('FPT', 'admin@fpt.vn', 'admin123', 'Nguyễn Văn Hưng (Admin FPT)', 'HR', 'TENANT_ADMIN', 15, 0, 36)
    """)

    # 5. NHÂN VIÊN CỦA FPT
    cursor.execute("""
        INSERT INTO users (tenant_id, email, hashed_password, full_name, department, role, total_leave_days, used_leave_days, tenure_months)
        VALUES ('FPT', 'phong.it@fpt.vn', '123456', 'Lê Văn Phong', 'Engineering', 'EMPLOYEE', 12, 0, 12)
    """)

    # Bot của VinFast
    cursor.execute("""
        INSERT INTO agents (tenant_id, name, description, instruction, department_access)
        VALUES ('VINFAST', 'VinFast HR Policy Assistant', 'Trợ lý chính sách nhân sự & thủ tục nghỉ phép VinFast', 'Bạn là trợ lý nhân sự VinFast, hỗ trợ tra cứu nội quy và xin nghỉ phép.', 'ALL')
    """)
    cursor.execute("""
        INSERT INTO agents (tenant_id, name, description, instruction, department_access)
        VALUES ('VINFAST', 'VinFast Marketing Brand Assistant', 'Trợ lý thương hiệu & nhận diện Marketing VinFast', 'Bạn là trợ lý giải đáp Brand Guideline và nội quy truyền thông Marketing VinFast.', 'Marketing')
    """)

    # Bot của FPT
    cursor.execute("""
        INSERT INTO agents (tenant_id, name, description, instruction, department_access)
        VALUES ('FPT', 'FPT Smart Workplace Assistant', 'Trợ lý vận hành nội bộ & hỗ trợ nhân viên FPT', 'Bạn là trợ lý ảo hỗ trợ công việc và quy chế FPT.', 'ALL')
    """)

    conn.commit()
    conn.close()
    print("✅ Đã thiết lập CSDL SaaS Multi-Tenant chuẩn 3 cấp bậc thành công!")

if __name__ == '__main__':
    init_clean_saas_db()
