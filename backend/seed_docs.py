import sqlite3

conn = sqlite3.connect('D:/mini-agent-studio/backend/database.db')
cursor = conn.cursor()

# 1. Thêm cột tenant_id vào bảng documents nếu chưa có
cursor.execute("PRAGMA table_info(documents)")
cols = [c[1] for c in cursor.fetchall()]
if 'tenant_id' not in cols:
    cursor.execute("ALTER TABLE documents ADD COLUMN tenant_id TEXT DEFAULT 'VINFAST'")

# 2. Xóa các tài liệu cũ và nạp lại chuẩn theo từng Tenant
cursor.execute("DELETE FROM documents")

# Tài liệu của VinFast
cursor.execute("""
    INSERT INTO documents (tenant_id, file_name, file_path, file_size_kb)
    VALUES ('VINFAST', 'Noi_quy_Phong_Marketing_VinFast.txt', 'D:/mini-agent-studio/data/Noi_quy_Phong_Marketing_VinFast.txt', 5)
""")
cursor.execute("""
    INSERT INTO documents (tenant_id, file_name, file_path, file_size_kb)
    VALUES ('VINFAST', 'Quy_che_Nhan_su_VinFast_2026.txt', 'D:/mini-agent-studio/data/Quy_che_Nhan_su_VinFast_2026.txt', 6)
""")
cursor.execute("""
    INSERT INTO documents (tenant_id, file_name, file_path, file_size_kb)
    VALUES ('VINFAST', 'Quy_che_Tai_chinh_Ke_toan.txt', 'D:/mini-agent-studio/data/Quy_che_Tai_chinh_Ke_toan.txt', 4)
""")

# Tài liệu mẫu cho FPT
cursor.execute("""
    INSERT INTO documents (tenant_id, file_name, file_path, file_size_kb)
    VALUES ('FPT', 'Quy_che_Lam_viec_FPT_Software.txt', 'D:/mini-agent-studio/data/Quy_che_Lam_viec_FPT_Software.txt', 4)
""")

conn.commit()
print("Documents table successfully updated with Tenant Isolation!")
cursor.execute("SELECT id, tenant_id, file_name FROM documents")
print(cursor.fetchall())
conn.close()
