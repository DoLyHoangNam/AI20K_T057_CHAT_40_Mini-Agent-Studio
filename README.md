# 🏢 MINI AGENT STUDIO — MULTI-DOMAIN AI AGENT SAAS PLATFORM
> **Dự án:** CHAT-40 — Nền tảng No-Code Khởi tạo & Điều phối AI Agent Đa Lĩnh Vực (Doanh nghiệp • Giáo dục • Y tế)  
> **Khóa đào tạo:** Phoenix AI20K - Cohort V | **Đội thi:** T057  
> **Công nghệ triển khai (MVP):** StateGraph Engine (`LangGraphAgent`) • Google Gemini API (`gemini-flash-latest` & `gemini-embedding-001` 3072-dim) • Keycloak OIDC SSO • SQLite 3 / MySQL 8.0 • Multi-Tenant & Unit ACL • Human-in-the-Loop (HITL)

---

## 📚 BỘ HỒ SƠ NỘP BÀI CHUẨN (PROJECT DELIVERABLES)

Toàn bộ 4 hạng mục tài liệu chuẩn của khóa học được lưu trữ trực tiếp tại thư mục gốc của Repository:

| STT | Hạng mục (Deliverable) | File Tài liệu | Mô tả nội dung chính |
| :---: | :--- | :--- | :--- |
| **01** | **Project Brief** | 📄 [`Brief.md`](./Brief.md) | Hồ sơ đề xuất dự án: Bối cảnh, Bài toán đa lĩnh vực, Giải pháp phân quyền đơn vị, Kiến trúc mục tiêu & Lộ trình. |
| **02** | **Product Requirements Document (PRD)** | 📘 [`PRD.md`](./PRD.md) | Đặc tả yêu cầu sản phẩm (v2.1): User Personas, Functional Requirements, Ma trận ACL 3 tầng, Schema CSDL, REST API & Bảng đối chiếu **MVP Hiện tại vs. Lộ trình Mở rộng (Roadmap)**. |
| **03** | **Wireframe & UI Flow** | 🎨 [`Wireframe_UI_Flow.md`](./Wireframe_UI_Flow.md) | Sơ đồ luồng điều hướng toàn hệ thống (Mermaid Flowchart), Sequence Diagram HITL & Bản vẽ ASCII Wireframe chi tiết cho 5 màn hình theo chuẩn **EduManage SaaS UI**. |
| **04** | **GitHub Repo & AI Log Setup** | 🤖 [`AI_Log.md`](./AI_Log.md) | Nhật ký ứng dụng AI xuyên suốt 5 giai đoạn phát triển (Prompt, Kết quả AI, Phần nhóm tự kiểm định/sửa lỗi) + Hướng dẫn cấu hình `backend/.env` & AI Trace Log. |

---

## 📌 I. GIỚI THIỆU DỰ ÁN
**Mini Agent Studio (CHAT-40)** là nền tảng SaaS Multi-Tenant cho phép Quản trị viên tổ chức (`TENANT_ADMIN`) tại các **Doanh nghiệp, Trường học và Bệnh viện** tự khởi tạo, cấu hình tính cách (System Prompt), nạp tài liệu PDF/TXT (Vector RAG) và phân quyền các **AI Agent chuyên biệt theo từng Đơn vị (`department`)** mà không cần viết code:

1. **Đa lĩnh vực linh hoạt (Multi-Domain Adaptive Schema):** Tự động thích ứng mô hình đơn vị và biểu mẫu nghiệp vụ theo từng loại hình tổ chức (`backend/schema_engine.py`):
   - 🏢 **Doanh nghiệp (`VINFAST`):** Phân theo *Phòng ban* (`Marketing`, `Accounting`, `Production`) — Nghiệp vụ *Đề xuất & Đơn xin nghỉ phép*.
   - 🎓 **Giáo dục (`VNU` - Vin University):** Phân theo *Khoa / Lớp học* (`Lớp AI - K68`) — Nghiệp vụ *Đơn học vụ / Xin vắng mặt*.
   - 🏥 **Y tế (`BVQT` - BV Đa khoa Quốc tế):** Phân theo *Chuyên khoa* (`Khoa Nội`, `Khoa Dược`) — Nghiệp vụ *Yêu cầu đổi ca trực*.
2. **Tra cứu tri thức chuẩn xác kèm trích dẫn (Pre-filtered Vector RAG):** Trích xuất văn bản PDF trực tiếp trên trình duyệt bằng **Mozilla PDF.js**, chia đoạn văn (`\n\n`, lọc đoạn $> 25$ ký tự), nhúng Vector 3.072 chiều (`models/gemini-embedding-001`) và tiền lọc theo cả `tenant_id` lẫn `department_access` trước khi tính **Cosine Similarity**.
3. **Cơ chế An toàn Human-in-the-Loop (HITL):** Tự động ngắt trạng thái (`interrupt_hitl = True`) khi phát hiện ý định trình ký/nộp đơn để người dùng kiểm tra và bấm xác nhận trước khi lưu `PENDING` vào CSDL và thông báo thời gian thực cho Quản trị viên.
4. **Phân quyền truy cập đa tầng (Zero Data Leakage):** Chốt chặn cứng tại cả giao diện, cổng API `/api/chat` (`ACL_DENIED`) và tầng truy vấn Vector (`backend/vector_store.py`).

---

## 🏗️ II. KIẾN TRÚC KỸ THUẬT THỰC TẾ (IMPLEMENTED ARCHITECTURE)

```
[ FRONTEND CLIENT — EDUMANAGE SAAS DASHBOARD UI (frontend/) ]
  ├── login.html             : Cổng xác thực Keycloak OIDC SSO + Bộ chuyển vai Demo nhanh (Role Switcher)
  ├── super_admin.html       : Cổng Chủ nền tảng (Cấp phát Tenant mới, Đồng bộ Keycloak & Gửi mail SMTP)
  ├── admin_studio.html      : No-Code Agent Studio (13+ Mẫu Agent), Quản lý Đơn vị/CSV, Kho RAG, Duyệt HITL
  ├── employee_portal.html   : Cổng Chat AI theo Đơn vị, Hồ sơ động (Dynamic Schema), Xác nhận HITL & Toast
  └── database_viewer.html   : Trình duyệt 5 bảng CSDL SQLite trực quan thời gian thực
         │
         ▼ (HTTP REST API / JSON)
[ UNIFIED BACKEND SERVER (backend/server.py — ThreadingHTTPServer) ]
  ├── CSDL Quan Hệ (backend/database.db - SQLite 3): tenants, users, agents, documents, leave_requests
  ├── Động cơ Giao diện Đa ngành (backend/schema_engine.py): ENTERPRISE / EDUCATION / HEALTHCARE / CUSTOM
  ├── Đồng bộ IAM & Email (Keycloak REST API port 8080 + Gmail SMTP backend/mailer.py)
  └── Lõi Đồ Thị Trạng Thái (backend/agent_engine.py — LangGraphAgent):
         ├── Bước 0 (Server Guardrail): Kiểm tra xác thực & Chốt chặn Unit ACL (user.department == agent.department_access)
         ├── Node 1 (Intent & HITL Node): Phân loại ý định (RAG_SEARCH vs CREATE_REQUEST) & Kích hoạt HITL Interrupt
         └── Node 2 (Vector RAG & LLM Node): Pre-filtering Vector Search (Cosine > 0.35) + Gemini Flash (gemini-flash-latest) + Citation
         │
         ▼
[ VECTOR DATABASE (backend/vector_store.py & backend/vector_index.json) ]
  └── Vector Index 3.072 Chiều (models/gemini-embedding-001) — Cô lập theo tenant_id & department
```

---

## 🚀 III. HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY (QUICK START)

### 1. Cấu hình biến môi trường (`backend/.env`)
Tạo file `backend/.env` (xem mẫu tại `backend/.env.example`):
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
SMTP_USER=your_gmail@gmail.com
SMTP_PASS=your_google_app_password
KC_ADMIN_PASS=admin123
```

### 2. Khởi chạy Backend Server
Mở **PowerShell** hoặc **Terminal** tại thư mục gốc dự án và chạy:
```powershell
python D:\mini-agent-studio\backend\server.py
```
Truy cập ứng dụng tại: 👉 **`http://localhost:8000/login.html`**

### 3. Hai chế độ Đăng nhập & Trải nghiệm Demo
- **Chế độ 1 — Chuyển vai Demo Nhanh (Role Switcher - Không cần bật Docker):** Ngay tại màn hình `login.html`, bấm trực tiếp vào một trong các nút dưới mục **⚡ CHUYỂN VAI DEMO NHANH (ROLE SWITCHER)** để vào thẳng giao diện của từng vai trò trong 1 giây.
- **Chế độ 2 — Xác thực Tập trung qua Keycloak OIDC SSO:** Khi khởi chạy Docker container Keycloak tại `http://localhost:8080` (Realm `mini-agent-platform`, Client `mini-agent-studio-app`), bấm nút **Đăng nhập bằng Keycloak SSO** để xác thực OIDC chuẩn doanh nghiệp.

---

## 👥 IV. DANH SÁCH TÀI KHOẢN CÓ SẴN TRONG CSDL (`backend/database.db`)

| Tổ chức (`tenant_id`) | Tài khoản (`email`) | Vai trò (`role`) | Đơn vị (`department`) | Kịch bản kiểm thử chính |
| :--- | :--- | :---: | :---: | :--- |
| 🌐 **`PLATFORM`** | `dolyhoangnam13072005@gmail.com` | `SUPER_ADMIN` | `Executive` | Cấp bản quyền Tổ chức mới (Doanh nghiệp/Giáo dục/Y tế), đồng bộ Keycloak & SMTP. |
| 🏢 **`VINFAST`** | `admin@vinfast.vn` | `TENANT_ADMIN` | `Executive` | Tạo Agent theo phòng ban, tải PDF quy chế, nhập CSV nhân sự, duyệt đơn HITL. |
| 🏢 **`VINFAST`** | `marketing@vinfast.vn` | `EMPLOYEE` | `Marketing` | Mở khóa `Trợ lý Phòng Marketing`, tra cứu Brand Guideline (Cosine ~0.87), gửi HITL. |
| 🏢 **`VINFAST`** | `ketoan@vinfast.vn` | `EMPLOYEE` | `Accounting` | Mở khóa `Trợ lý Phòng Kế toán`, tra cứu định mức công tác phí & hóa đơn VAT. |
| 🏢 **`VINFAST`** | `nam.dlh@vinfast.vn` | `EMPLOYEE` | `Production` | Chỉ dùng được Agent `ALL`; bị khóa cứng (`ACL_DENIED`) khi bấm sang Marketing/Kế toán. |
| 🎓 **`VNU`** *(VinUni)* | `phonghoangthe112@gmail.com` | `TENANT_ADMIN` | `Executive` | Quản trị viên Trường ĐH VinUni: Tạo Trợ giảng theo Lớp/Khoa, duyệt đơn học vụ. |
| 🎓 **`VNU`** *(VinUni)* | `sv.ai@vnu.edu.vn` | `EMPLOYEE` | `Lớp AI - K68` | Sinh viên Lớp AI - K68: Xem hồ sơ tín chỉ động, chat với `Trợ Giảng Lớp AI - K68`. |
| 🏥 **`BVQT`** *(Bệnh viện)* | `admin@benhvien.vn` | `TENANT_ADMIN` | `Executive` | Quản trị viên Bệnh viện: Quản lý Chuyên khoa, duyệt yêu cầu đổi ca trực. |
| 🏥 **`BVQT`** *(Bệnh viện)* | `bs.noi@benhvien.vn` | `EMPLOYEE` | `Khoa Nội` | Bác sĩ Khoa Nội: Xem định mức ca trực tháng, gửi yêu cầu đổi ca trực qua HITL. |
