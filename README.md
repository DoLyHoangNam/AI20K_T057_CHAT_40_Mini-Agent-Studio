# 🏢 MINI AGENT STUDIO — MULTI-DOMAIN AI AGENT SAAS PLATFORM
> **Dự án:** CHAT-40 — Nền tảng Tạo & Điều Phối AI Agent Đa Lĩnh Vực (Doanh nghiệp • Giáo dục • Y tế)  
> **Khóa đào tạo:** Phoenix AI20K - Cohort V | **Đội thi:** T057  
> **Công nghệ chủ đạo:** LangGraph Architecture • Google Gemini API • Vector Database (Gemini-Embeddings 3072-dim) • SQLite/MySQL • Multi-Tenant RBAC/ABAC • Human-In-The-Loop (HITL)

---

## 📚 BỘ HỒ SƠ NỘP BÀI CHUẨN (PROJECT DELIVERABLES)

Toàn bộ 4 hạng mục tài liệu chuẩn của khóa học được lưu trữ trực tiếp tại thư mục gốc của Repository:

| STT | Hạng mục (Deliverable) | File Tài liệu | Mô tả nội dung chính |
| :---: | :--- | :--- | :--- |
| **01** | **Project Brief** | 📄 [`Brief.md`](./Brief.md) | Hồ sơ đề xuất dự án 6 phần: Tổng quan, Bài toán, Giải pháp Đa lĩnh vực, Kiến trúc 3 tầng, Công nghệ & Lộ trình. |
| **02** | **Product Requirements Document (PRD)** | 📘 [`PRD.md`](./PRD.md) | Đặc tả yêu cầu sản phẩm chi tiết: User Personas, Functional Requirements (FR), Non-Functional Requirements (NFR), Ma trận ACL 2 lớp, Schema CSDL & REST API. |
| **03** | **Wireframe & UI Flow** | 🎨 [`Wireframe_UI_Flow.md`](./Wireframe_UI_Flow.md) | Sơ đồ luồng điều hướng toàn hệ thống (Mermaid Flowchart), Sequence Diagram HITL & Bản vẽ ASCII Wireframe chi tiết cho 5 màn hình theo chuẩn **EduManage SaaS UI**. |
| **04** | **GitHub Repo & AI Log Setup** | 🤖 [`AI_Log.md`](./AI_Log.md) | Nhật ký ứng dụng AI xuyên suốt 5 giai đoạn phát triển (Prompt, Kết quả AI, Phần nhóm tự kiểm chứng/chỉnh sửa) + Hướng dẫn cấu hình `.env` & AI Trace Log. |

---

## 📌 I. GIỚI THIỆU DỰ ÁN
**Mini Agent Studio** là nền tảng SaaS Multi-Tenant cho phép người dùng nghiệp vụ (Creator/Organization Admin) tại các **Doanh nghiệp, Trường học và Bệnh viện** tự xây dựng, cấu hình tính cách, nạp tài liệu huấn luyện (RAG) và xuất bản các **AI Agent chuyên biệt** mà không cần viết code (No-Code Builder).

Hệ thống giải quyết trọn vẹn 4 bài toán cốt lõi:
1. **Đa lĩnh vực linh hoạt (Multi-Domain Adaptive):** Tự động thích ứng mô hình đơn vị và nghiệp vụ theo từng loại hình tổ chức:
   - 🏢 **Doanh nghiệp (VinFast):** Phân theo *Phòng ban* (Sản xuất, Marketing, Kế toán, HR) — Nghiệp vụ *Đơn xin nghỉ phép*.
   - 🎓 **Giáo dục (ĐH Bách Khoa):** Phân theo *Lớp / Khoa* (CNTT K68, Điện - Điện tử, Đào tạo) — Nghiệp vụ *Đơn xin nghỉ học / bảo lưu*.
   - 🏥 **Y tế (BV Đa khoa Quốc tế):** Phân theo *Chuyên khoa* (Khoa Nội, Khoa Ngoại, Khoa Dược) — Nghiệp vụ *Đơn xin đổi ca trực*.
2. **Tra cứu tri thức chuẩn xác kèm trích dẫn (Vector RAG):** Đọc trực tiếp văn bản quy chế, quy trình, phác đồ và đối sánh Cosine Similarity trên Vector 3,072 chiều (`models/gemini-embedding-001`).
3. **Cơ chế An toàn Human-In-The-Loop (HITL):** Tự động ngắt trạng thái (`State Interrupt`) để người dùng kiểm tra và bấm xác nhận trước khi ghi nhận phiếu/đơn vào CSDL.
4. **Phân quyền truy cập đa tầng (2-Layer ACL Security):** Cô lập dữ liệu tuyệt đối giữa các Tổ chức (`tenant_id`) và kiểm soát quyền truy cập Agent/Tài liệu theo Đơn vị trực thuộc (`allowed_depts`).

---

## 🏗️ II. KIẾN TRÚC KỸ THUẬT (SYSTEM ARCHITECTURE)

```
[ FRONTEND CLIENT — EDUMANAGE SAAS DASHBOARD UI ]
  ├── login.html             : Cổng đăng nhập hợp nhất & Chọn nhanh tài khoản Demo đa ngành
  ├── super_admin.html       : Cổng Quản trị Nền tảng (Tạo Tổ chức Doanh nghiệp/Trường học/Y tế, Duyệt nâng cấp gói)
  ├── admin_studio.html      : No-Code Agent Studio, Quản lý Thành viên/Đơn vị, Kho RAG, Duyệt Đơn & AI Trace Log
  ├── employee_portal.html   : Cổng tương tác Chat AI đa năng, Hồ sơ phép, Xác nhận HITL & Thông báo Real-time
  └── database_viewer.html   : Trình xem CSDL trực quan (Database Explorer)
         │
         ▼ (HTTP REST API / JSON)
[ UNIFIED BACKEND SERVER (backend/server.py) ]
  ├── CSDL Quan Hệ (database.db - SQLite / MySQL 8.0): tenants, users, agents, documents, leave_requests
  └── Lõi Đồ Thị Trạng Thái LangGraph (backend/agent_engine.py):
         ├── Node 1: IntentClassifierNode (Phân loại ý định & Kiểm tra ACL)
         ├── Node 2: LeavePolicyToolNode (Truy vấn CSDL & tính toán ngày phép thực tế)
         ├── Node 3: VectorRAGRetrievalNode (Cosine Similarity trên Vector DB + Pre-retrieval ACL Filter)
         ├── Node 4: HITLInterruptNode (Tạm dừng luồng chờ người dùng xác nhận)
         └── Node 5: LLMResponseGenerationNode (Google Gemini 2.5 Flash + Gắn trích dẫn nguồn)
         │
         ▼
[ VECTOR DATABASE (backend/vector_store.py) ]
  └── Vector Index 3,072 Chiều (models/gemini-embedding-001)
      ├── Noi_quy_Phong_Marketing_VinFast.txt
      ├── Quy_che_Nhan_su_VinFast_2026.txt
      └── Quy_che_Tai_chinh_Ke_toan.txt
```

---

## 🚀 III. HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY (QUICK START)

### 1. Yêu cầu môi trường
- Hệ điều hành: Windows 10/11, macOS hoặc Linux
- Python: Phiên bản `3.10` trở lên
- Kết nối Internet (để gọi Google Gemini API; hệ thống có sẵn cơ chế Fallback thông minh nếu chạy Offline)

### 2. Cấu hình API Key (Tùy chọn)
Tạo file `backend/.env` với nội dung:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
PORT=8000
```

### 3. Khởi chạy hệ thống chỉ với 1 lệnh
Mở **PowerShell** hoặc **Terminal** tại thư mục dự án và chạy:

```powershell
python backend/server.py
```

Server sẽ tự động khởi động tại địa chỉ:
👉 **`http://localhost:8000/login.html`**

---

## 👥 IV. TÀI KHOẢN TRẢI NGHIỆM HỆ THỐNG (DEMO ACCOUNTS)

| Phân hệ / Lĩnh vực | Tài khoản (Email) | Mật khẩu | Vai trò (Role) | Phạm vi quyền hạn (ACL Scope) |
| :--- | :--- | :---: | :---: | :--- |
| 🌐 **Platform Super Admin** | `superadmin@platform.vn` | `super123` | **SUPER_ADMIN** | Quản trị toàn nền tảng: Tạo tổ chức mới (Doanh nghiệp/Giáo dục/Y tế), duyệt nâng cấp gói cước. |
| 🏢 **Doanh nghiệp (VinFast)** | `admin@vinfast.vn` | `admin123` | **ADMIN** | Quản trị viên VinFast: Tạo Agent, quản lý nhân sự, duyệt đơn nghỉ phép, giám sát AI Log. |
| 🏢 **Doanh nghiệp (VinFast)** | `nam.dlh@vinfast.vn` | `123456` | **EMPLOYEE** | Kỹ sư Sản xuất: Tra cứu nội quy chung, tạo đơn nghỉ phép qua HITL (bị chặn Bot Kế toán). |
| 🏢 **Doanh nghiệp (VinFast)** | `marketing@vinfast.vn` | `123456` | **EMPLOYEE** | Chuyên viên Marketing: Truy cập Trợ lý Marketing, tra cứu Brand Guideline. |
| 🏢 **Doanh nghiệp (VinFast)** | `ketoan@vinfast.vn` | `123456` | **EMPLOYEE** | Kế toán viên: Được cấp quyền truy cập Bot Kế toán & Hóa đơn mật. |
| 🎓 **Giáo dục (ĐH Bách Khoa)** | `admin@bachkhoa.edu.vn` | `admin123` | **ADMIN** | Quản trị viên Nhà trường: Quản lý Khoa/Lớp, tạo Trợ lý Học vụ, duyệt đơn xin nghỉ học. |
| 🎓 **Giáo dục (ĐH Bách Khoa)** | `sv.cntt@bachkhoa.edu.vn` | `123456` | **EMPLOYEE** | Sinh viên Lớp CNTT K68: Hỏi đáp quy chế tín chỉ, học bổng, gửi đơn xin phép nghỉ học. |
| 🏥 **Y tế (BV Quốc tế)** | `admin@benhvien.vn` | `admin123` | **ADMIN** | Quản trị viên Bệnh viện: Quản lý Chuyên khoa, tạo Trợ lý Y khoa, duyệt đơn đổi ca trực. |
| 🏥 **Y tế (BV Quốc tế)** | `bs.noi@benhvien.vn` | `123456` | **EMPLOYEE** | Bác sĩ Khoa Nội: Tra cứu phác đồ điều trị, danh mục thuốc BHYT, gửi yêu cầu đổi ca trực. |

---

## 🧪 V. KỊCH BẢN KIỂM THỬ MẪU (TEST CASES)

1. **Test RAG Tra cứu Vector DB:**
   - Đăng nhập `marketing@vinfast.vn` ➔ Hỏi: *"Logo VinFast được phép đặt trên nền màu gì?"*
   - *Kết quả:* Agent trích xuất chính xác Điều 1 Brand Guideline kèm Score Cosine Similarity `~0.87`.
2. **Test ACL Phân quyền 2 lớp:**
   - Đăng nhập `nam.dlh@vinfast.vn` (Phòng Sản xuất) ➔ Bấm vào *Trợ lý Kế toán & Hóa đơn* hoặc hỏi về định mức công tác phí mật của phòng Kế toán.
   - *Kết quả:* Hệ thống kích hoạt cảnh báo chặn truy cập bảo mật (`ACL Blocked`), không rò rỉ dữ liệu.
3. **Test Quy trình HITL & Phê duyệt tự động đa lĩnh vực:**
   - Đăng nhập Nhân viên / Sinh viên / Bác sĩ ➔ Chat yêu cầu xin nghỉ phép / nghỉ học / đổi ca trực ➔ Bấm nút **Xác nhận gửi đơn (HITL)**.
   - Mở tab Admin của tổ chức tương ứng (`admin_studio.html`) ➔ Bấm **Duyệt đơn**.
   - Tab Người dùng lập tức nhận thông báo Real-time và CSDL tự động khấu trừ số ngày phép còn lại.
