# 🏢 MINI AGENT STUDIO — ENTERPRISE AI AGENT PLATFORM
> **Dự án:** CHAT-40 — Nền tảng Tạo & Điều Phối AI Agent Đa Năng Doanh Nghiệp (VinFast Tenant)  
> **Khóa đào tạo:** Phoenix AI20K - Cohort V | **Đội thi:** T057  
> **Công nghệ chủ đạo:** LangGraph Architecture • Google Gemini API • Vector Database (Gemini-Embeddings 3072-dim) • SQLite • Human-In-The-Loop (HITL)

---

## 📌 I. GIỚI THIỆU DỰ ÁN
**Mini Agent Studio** là giải pháp nền tảng cho phép người dùng nghiệp vụ (Creator/Admin) tự xây dựng, cấu hình tính cách và xuất bản các **AI Agent nghiệp vụ** mà không cần lập trình (No-Code Builder).

Hệ thống giải quyết bài toán vận hành nội bộ quy mô lớn tại doanh nghiệp (Thực nghiệm trên kịch bản Tập đoàn VinFast):
1. **Tra cứu quy chế & nội quy đa phòng ban (RAG):** Đọc trực tiếp các văn bản quy định của Marketing, Tài chính Kế toán và Nhân sự với độ chính xác cao kèm trích dẫn văn bản chuẩn xác.
2. **Quản trị phép năm & Thao tác nghiệp vụ tự động (Tools Integration):** Kết nối CSDL SQLite đọc hồ sơ thâm niên, tính ngày phép còn lại theo thời gian thực.
3. **Cơ chế An toàn Human-In-The-Loop (HITL):** Tự động ngắt trạng thái (`State Interrupt`) để người dùng kiểm tra và bấm xác nhận trước khi gửi đơn lên Quản lý.
4. **Phân quyền truy cập đa tầng (ACL Security):** Tự động cô lập tri thức và công cụ theo phòng ban (Nhân viên xưởng sản xuất không thể truy cập tài liệu tài chính của phòng Kế toán).

---

## 🏗️ II. KIẾN TRÚC KỸ THUẬT (SYSTEM ARCHITECTURE)

```
[ FRONTEND CLIENT ]
  ├── login.html             : Đăng nhập phân quyền (Admin / Sản xuất / Marketing / Kế toán)
  ├── employee_portal.html   : Cổng tương tác chat, nhận thông báo thời gian thực & hồ sơ phép
  ├── admin_studio.html      : No-Code Agent Studio, Hộp thư duyệt đơn & Giám sát Langfuse
  └── database_viewer.html   : Trình xem CSDL thời gian thực (Database Explorer)
         │
         ▼ (HTTP REST API / JSON)
[ UNIFIED BACKEND SERVER (server.py) ]
  ├── CSDL Quan Hệ (database.db - SQLite): users, agents, documents, leave_requests
  └── Lõi Đồ Thị Trạng Thái LangGraph (agent_engine.py):
         ├── Node 1: IntentClassifierNode (Phân loại ý định)
         ├── Node 2: LeavePolicyToolNode (Truy vấn CSDL nhân sự)
         ├── Node 3: VectorRAGRetrievalNode (Cosine Similarity trên Vector DB)
         ├── Node 4: HITLInterruptNode (Dừng chờ xác nhận đơn)
         └── Node 5: LLMResponseGenerationNode (Mô hình Google Gemini Flash)
         │
         ▼
[ VECTOR DATABASE (vector_store.py) ]
  └── Vector Index 3,072 Chiều (models/gemini-embedding-001)
      ├── Noi_quy_Phong_Marketing_VinFast.txt
      ├── Quy_che_Nhan_su_VinFast_2026.txt
      └── Quy_che_Tai_chinh_Ke_toan.txt
```

---

## 🚀 III. HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY (QUICK START)

### 1. Yêu cầu môi trường
- Hệ điều hành: Windows 10/11
- Python: Phiên bản 3.10 trở lên
- Kết nối Internet (để kết nối Google Gemini API)

### 2. Khởi chạy hệ thống chỉ với 1 lệnh
Mở **PowerShell** hoặc **Command Prompt** tại thư mục dự án và chạy:

```powershell
python D:\mini-agent-studio\backend\server.py
```

Server sẽ tự động khởi động tại địa chỉ:
👉 **`http://localhost:8000/`**

---

## 👥 IV. TÀI KHOẢN TRẢI NGHIỆM HỆ THỐNG

| Tài khoản (Email) | Mật khẩu | Vai trò (Role) | Phạm vi quyền hạn (ACL Scope) |
| :--- | :---: | :---: | :--- |
| **admin@vinfast.vn** | `admin123` | **ADMIN** | Quản trị toàn quyền: Tạo Agent mới, Duyệt/Từ chối đơn xin nghỉ phép, Giám sát hệ thống. |
| **nam.dlh@vinfast.vn** | `123456` | **EMPLOYEE** | Nhân viên Sản xuất: Tiêu chuẩn 8 ngày phép (thâm niên 8 tháng), chỉ xem tài liệu nội quy chung. |
| **marketing@vinfast.vn** | `123456` | **EMPLOYEE** | Nhân viên Marketing: Truy cập Trợ lý Marketing, tra cứu Brand Guideline, quy chuẩn logo. |
| **ketoan@vinfast.vn** | `123456` | **EMPLOYEE** | Nhân viên Kế toán: Được cấp quyền truy cập Bot Kế Toán Mật (công tác phí, hóa đơn VAT). |

---

## 🧪 V. KỊCH BẢN KIỂM THỬ MẪU (TEST CASES)

1. **Test RAG Tra cứu Vector DB:**
   - Đăng nhập `marketing@vinfast.vn` ➔ Hỏi: *"Logo VinFast được phép đặt trên nền màu gì?"*
   - *Kết quả:* Agent trích xuất chính xác Điều 1 Brand Guideline kèm Score Cosine Similarity ~0.87.
2. **Test ACL Phân quyền:**
   - Đăng nhập `nam.dlh@vinfast.vn` (Sản xuất) ➔ Bấm vào *Trợ lý Kế toán & Hóa đơn* ở cột trái.
   - *Kết quả:* Hệ thống kích hoạt cảnh báo chặn truy cập bảo mật.
3. **Test Quy trình HITL & Phê duyệt tự động:**
   - Nhân viên gửi: *"Tôi muốn xin nghỉ 1 ngày"* ➔ Nhập ngày & lý do ➔ Bấm xác nhận HITL.
   - Mở tab Admin tại `admin_studio.html` ➔ Bấm **Duyệt đơn**.
   - Tab Nhân viên lập tức nhận thông báo Popup thời gian thực và CSDL tự động trừ ngày phép.
