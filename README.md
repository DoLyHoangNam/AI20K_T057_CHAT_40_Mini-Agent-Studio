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
  ├── login.html             : Cổng xác thực tập trung Keycloak OIDC SSO (Realm: mini-agent-platform)
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

### 3. Xác thực Tập trung qua Keycloak OIDC SSO
- Khởi chạy Docker container Keycloak tại `http://localhost:8080` (Realm `mini-agent-platform`, Client `mini-agent-studio-app`).
- Tại màn hình `http://localhost:8000/login.html`, bấm nút **Đăng nhập bằng Keycloak SSO** để xác thực OIDC chuẩn doanh nghiệp và tự động điều hướng theo vai trò (`SUPER_ADMIN`, `TENANT_ADMIN`, `EMPLOYEE`).

---

## 👥 IV. QUY TRÌNH DEMO END-TO-END BẰNG EMAIL THẬT & KEYCLOAK SSO

Hệ thống được thiết lập ở trạng thái **Clean Enterprise State** — khởi đầu chỉ với **duy nhất 1 tài khoản Chủ nền tảng (`SUPER_ADMIN`)** trên cả Keycloak và CSDL để trình diễn trọn vẹn luồng cấp phát tự động từ con số 0:

### Bước 1: Đăng nhập Chủ nền tảng (`SUPER_ADMIN`)
- Truy cập `http://localhost:8000/login.html` $\rightarrow$ Bấm **Đăng nhập bằng Keycloak SSO**.
- Nhập tài khoản gốc:
  - **Email:** `dolyhoangnam13072005@gmail.com`
  - **Mật khẩu:** `Admin@123`
- Hệ thống tự động điều hướng vào `super_admin.html`. Tại đây, nhập Mã tổ chức (VD: `VINFAST` hoặc `VNU`), chọn Lĩnh vực (`ENTERPRISE` / `EDUCATION` / `HEALTHCARE`) và nhập **Email Gmail thật của Quản trị viên Tổ chức**.
- Hệ thống tự động khởi tạo tài khoản `TENANT_ADMIN` trên Keycloak và **gửi mật khẩu ngẫu nhiên trực tiếp về hộp thư Gmail thật**.

### Bước 2: Đăng nhập Quản trị viên Tổ chức (`TENANT_ADMIN`)
- Mở hộp thư Gmail vừa nhận $\rightarrow$ Copy mật khẩu khởi tạo và đăng nhập qua Keycloak SSO để vào `admin_studio.html`.
- Thực hiện:
  1. **Thêm Thành viên & Đơn vị (`#tab-employees`):** Nhập Gmail thật của các thành viên trong nhóm (hoặc tải file CSV), phân vào các Phòng ban / Khoa / Lớp học khác nhau (VD: `Marketing`, `Accounting`, `Lớp AI - K68`). Hệ thống tiếp tục đồng bộ lên Keycloak và gửi mật khẩu về từng Gmail.
  2. **Khởi tạo Agent & Nạp PDF RAG (`#tab-builder`):** Chọn mẫu Agent theo đơn vị, tải file `.pdf` / `.txt` quy chế nội bộ để nhúng Vector 3.072 chiều và bấm **Xuất bản Agent**.

### Bước 3: Đăng nhập Thành viên Đơn vị (`EMPLOYEE`) & Kiểm chứng Bảo mật
- Thành viên dùng mật khẩu nhận qua Gmail đăng nhập vào `employee_portal.html`:
  - **Tra cứu Vector RAG:** Hỏi đáp quy chế của đơn vị mình (kèm hộp trích dẫn nguồn và điểm Cosine Similarity).
  - **Kiểm chứng Chặn ACL (`ACL_DENIED`):** Thử truy cập Agent hoặc hỏi tài liệu của phòng ban/lớp học khác $\rightarrow$ Hệ thống lập tức khóa và từ chối truy xuất.
  - **Trình ký HITL thời gian thực:** Gửi yêu cầu phê duyệt trong khung chat $\rightarrow$ Bấm xác nhận HITL $\rightarrow$ Quản trị viên bấm **Duyệt** bên `admin_studio.html` $\rightarrow$ Thành viên nhận thông báo Toast thời gian thực.
