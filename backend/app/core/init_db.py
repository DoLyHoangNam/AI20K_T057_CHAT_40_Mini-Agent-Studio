import os
import hashlib
from app.core.database import engine, Base, SessionLocal
from app.core.models import User, Agent, Document

def hash_password(password: str) -> str:
    """Mã hóa mật khẩu an toàn bằng SHA-256"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_database():
    print("⏳ [DATABASE]: Đang khởi tạo các bảng dữ liệu...")
    # Tạo tất cả các bảng: users, agents, documents, chat_logs
    Base.metadata.create_all(bind=engine)
    print("✅ [DATABASE]: Đã tạo bảng thành công!")

    db = SessionLocal()
    try:
        # Kiểm tra xem đã có dữ liệu chưa
        if db.query(User).first():
            print("ℹ️ [DATABASE]: Dữ liệu người dùng đã tồn tại. Bỏ qua bước nạp seed.")
            return

        print("🌱 [DATABASE]: Đang nạp dữ liệu mẫu ban đầu (Enterprise Seed Data)...")

        # 1. Tạo tài khoản Admin tối cao (HR Lead VinFast)
        admin_user = User(
            email="admin@vinfast.vn",
            hashed_password=hash_password("admin123"),
            full_name="Quản Trị Viên Nhân Sự VinFast",
            department="HR",
            role="ADMIN"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        # 2. Tạo 2 tài khoản nhân viên thuộc 2 phòng ban khác nhau (để test ACL phân quyền)
        employee_tech = User(
            email="nam.dlh@vinfast.vn",
            hashed_password=hash_password("user123"),
            full_name="Đỗ Lý Hoàng Nam",
            department="Production", # Phòng Sản xuất / Kỹ thuật
            role="EMPLOYEE"
        )
        employee_acc = User(
            email="ketoan@vinfast.vn",
            hashed_password=hash_password("user123"),
            full_name="Nguyễn Thị Lan",
            department="Accounting", # Phòng Kế toán
            role="EMPLOYEE"
        )
        db.add_all([employee_tech, employee_acc])
        db.commit()

        # 3. Tạo 2 con Agent đầu tiên đại diện cho 2 phòng ban
        bot_hr = Agent(
            name="VinFast HR Policy Assistant",
            description="Trợ lý giải đáp nội quy, tính ngày phép và hỗ trợ tạo đơn nghỉ phép",
            instruction="Bạn là trợ lý nhân sự VinFast, hỗ trợ giải đáp nội quy lao động, tính ngày phép và tạo đơn nghỉ phép.",
            department_access="ALL", # Ai cũng được dùng bot này
            creator_id=admin_user.id,
            is_published=True
        )
        bot_accounting = Agent(
            name="Trợ Lý Kế Toán & Hóa Đơn VinFast",
            description="Trợ lý nghiệp vụ kế toán, giải ngân, tạm ứng và đối soát hóa đơn",
            instruction="Bạn là trợ lý kế toán chuyên hỗ trợ đối soát hóa đơn, chi phí công tác và quy chế tài chính.",
            department_access="Accounting", # CHỈ PHÒNG KẾ TOÁN MỚI ĐƯỢC DÙNG
            creator_id=admin_user.id,
            is_published=True
        )
        db.add_all([bot_hr, bot_accounting])
        db.commit()

        print("==================================================================")
        print("🎉 [HOÀN TẤT]: DATABASE ĐÃ ĐƯỢC DỰNG THÀNH CÔNG VỚI 3 TÀI KHOẢN!")
        print("1. Admin tối cao: admin@vinfast.vn | Pass: admin123 (Role: ADMIN)")
        print("2. Nhân viên Sản xuất: nam.dlh@vinfast.vn | Pass: user123 (Dept: Production)")
        print("3. Nhân viên Kế toán: ketoan@vinfast.vn | Pass: user123 (Dept: Accounting)")
        print("==================================================================")

    finally:
        db.close()

if __name__ == "__main__":
    init_database()
