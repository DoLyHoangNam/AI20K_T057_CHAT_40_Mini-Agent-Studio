import sqlite3

conn = sqlite3.connect('D:/mini-agent-studio/backend/database.db')
cursor = conn.cursor()

print("📊 [CÁC BẢNG TRONG DATABASE]:")
for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
    print("  📁", row[0])

print("\n👥 [DANH SÁCH TÀI KHOẢN & PHÂN QUYỀN]:")
for row in cursor.execute("SELECT id, email, full_name, department, role FROM users;").fetchall():
    print(f"  • ID {row[0]}: {row[1]} | Tên: {row[2]} | Phòng: {row[3]} | Quyền: {row[4]}")

print("\n🤖 [DANH SÁCH CÁC CON BOT ĐÃ KHỞI TẠO]:")
for row in cursor.execute("SELECT id, name, department_access FROM agents;").fetchall():
    print(f"  • Bot ID {row[0]}: {row[1]} (Phạm vi truy cập: {row[2]})")

conn.close()
