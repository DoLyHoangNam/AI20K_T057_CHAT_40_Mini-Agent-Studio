# PRODUCT REQUIREMENTS DOCUMENT (PRD) — MINI AGENT STUDIO (CHAT-40)

* **Tên sản phẩm:** Mini Agent Studio — Nền tảng No-Code khởi tạo AI Agent đa lĩnh vực, xử lý đan xen hội thoại & phân quyền theo đơn vị
* **Mã đề tài:** CHAT-40 | **Đội ngũ phát triển:** AI20K - Team T057
* **Phiên bản:** v2.1 (Đồng bộ Thực tế Codebase Demo 1 & Lộ trình Mở rộng) | **Trạng thái:** Ready for Review

---

## 1. Tóm tắt Điều hành (Executive Summary)

**Mini Agent Studio (CHAT-40)** là nền tảng SaaS Multi-Tenant & Multi-Domain cho phép Quản trị viên của bất kỳ tổ chức nào (**Doanh nghiệp, Trường học, Bệnh viện, Tổ chức**) tự khởi tạo, cấu hình và phân quyền các **Trợ lý AI chuyên biệt theo từng Đơn vị (`department`)** mà không cần viết code:
* **Khối Doanh nghiệp (`ENTERPRISE`):** Chia theo Phòng ban (*Marketing, Kế toán - Tài chính, Nhân sự - HR, Kỹ thuật - IT, Kinh doanh - Sales...*).
* **Khối Giáo dục (`EDUCATION`):** Chia theo Khoa / Lớp học / Phòng chức năng (*Lớp AI - K68, Khoa CNTT, Khoa Kinh tế, Phòng Đào tạo, Công tác Sinh viên, Thư viện...*).
* **Khối Y tế & Tổ chức (`HEALTHCARE` / `CUSTOM`):** Chia theo Chuyên khoa / Bộ phận (*Khoa Nội, Khoa Khám bệnh, Khoa Dược, Hành chính viện...*).

Bên cạnh giao diện **No-Code Studio Builder**, nền tảng giải quyết các bài toán kỹ thuật cốt lõi:
1. **Cô lập dữ liệu đa tầng (3-Layer RBAC & Unit ACL)** trên kho tri thức Vector 3.072 chiều (`models/gemini-embedding-001`) ở cả tầng API lẫn tầng tiền lọc Vector (`Pre-retrieval Filter`).
2. **Trích dẫn nguồn chính xác (Citation Grounding)** & **Trạm phê duyệt con người (Human-in-the-Loop - HITL)** có thông báo thời gian thực.
3. **Động cơ Giao diện Đa ngành (Adaptive UI Schema Engine)** tự động biến đổi thẻ hồ sơ và biểu mẫu nghiệp vụ theo từng lĩnh vực tổ chức.

---

## 2. Chân dung Người dùng & Bài toán (User Personas & Use Cases)

| Nhóm người dùng | Mã Vai trò (`role`) | Đặc điểm & Nhu cầu cốt lõi |
| :--- | :--- | :--- |
| **1. Chủ nền tảng (Platform Owner)** | `SUPER_ADMIN` | Cấp bản quyền, khởi tạo không gian làm việc độc lập (`Tenant`) cho các Doanh nghiệp/Trường học/Bệnh viện mới, tự động đồng bộ tài khoản lên Keycloak SSO và gửi email bàn giao qua SMTP. |
| **2. Quản trị Tổ chức / Trưởng bộ phận / Giáo vụ** | `TENANT_ADMIN` | Không chuyên lập trình nhưng cần tạo nhanh các Agent theo từng Phòng ban / Khoa / Lớp học (qua 13+ Mẫu 1-Click hoặc tùy chỉnh), tải lên tài liệu PDF/TXT nội bộ, nhập danh sách thành viên (CSV) và phê duyệt đề xuất phát sinh từ luồng **HITL**. |
| **3. Thành viên / Nhân viên / Sinh viên / Bác sĩ** | `EMPLOYEE` | Truy cập cổng Chat để hỏi đáp quy chế, tài liệu chuyên môn hoặc bài giảng của đúng đơn vị mình (có trích dẫn nguồn), đồng thời gửi các đề xuất/đơn từ nghiệp vụ trình cấp quản lý phê duyệt. |

---

## 3. Ma trận Phân quyền Đa tầng (3-Layer RBAC & Unit ACL Matrix)

Mỗi người dùng được định danh bởi bộ 3 khóa: `tenant_id` (Tổ chức), `role` (Vai trò) và `department` (Đơn vị: Phòng ban / Khoa / Lớp học).

| Chức năng / Tài nguyên | `SUPER_ADMIN` | `TENANT_ADMIN` | `EMPLOYEE` (Thành viên đơn vị) |
| :--- | :---: | :---: | :---: |
| Khởi tạo / Xóa Tổ chức (`Tenants`) | ✅ Toàn quyền | ❌ | ❌ |
| Truy cập Studio Builder & Tạo Agent mới | ✅ | ✅ (Trong `tenant_id`) | ❌ (Chặn bởi Route Guard) |
| Tải tài liệu PDF/TXT & Vector hóa 3072-dim | ✅ | ✅ (Trong `tenant_id`) | ❌ |
| Thêm / Sửa / Xóa Thành viên & Nhập CSV | ✅ (Toàn hệ thống) | ✅ (Trong `tenant_id`) | ❌ |
| Chat với Agent toàn tổ chức (`department_access = ALL`) | ✅ | ✅ | ✅ (Chỉ truy xuất tài liệu `ALL` của đúng `tenant_id`) |
| Chat với Agent chuyên biệt (`department_access = X`) | ✅ | ✅ | ✅ **Chỉ khi `user.department == X`**<br>*(Ngược lại bị chặn `ACL_DENIED`)* |
| Khởi tạo đề xuất / yêu cầu phê duyệt (`HITL Request`) | ✅ | ✅ | ✅ (Trạng thái `PENDING`) |
| Phê duyệt / Từ chối đề xuất (`APPROVED` / `REJECTED`) | ✅ | ✅ (Approver) | ❌ |

---

## 4. Yêu cầu Chức năng (Functional Requirements)

### 4.1. Phân hệ Quản trị Nền tảng & Định danh SSO (`FR-01` -> `FR-03`)
* **`FR-01` (Keycloak OIDC SSO):** Xác thực tập trung qua Keycloak Server (`http://localhost:8080`, Realm `mini-agent-platform`), tự động ánh xạ sang hồ sơ SQLite nội bộ và điều hướng theo `role`.
* **`FR-02` (Multi-Tenant Provisioning):** `SUPER_ADMIN` khởi tạo tổ chức mới theo lĩnh vực (`ENTERPRISE`, `EDUCATION`, `HEALTHCARE`, `CUSTOM`), hệ thống tự động sinh cấu hình `ui_schema`, tạo tài khoản `TENANT_ADMIN` đầu tiên, đồng bộ lên Keycloak và gửi email bàn giao mật khẩu qua Gmail SMTP (`backend/mailer.py`).
* **`FR-03` (Bulk Member Provisioning):** `TENANT_ADMIN` thêm thành viên đơn lẻ hoặc tải file CSV/TXT hàng loạt (`Họ tên, Email, Đơn vị`), tự động gán quyền truy cập theo đơn vị.

### 4.2. Phân hệ No-Code Studio Builder & Kho Tri thức RAG (`FR-04` -> `FR-06`)
* **`FR-04` (Multi-Industry Agent Templates):** Cung cấp 13 mẫu Agent dựng sẵn cho 3 nhóm ngành (Doanh nghiệp: *Marketing, Kế toán, HR, IT, Sales*; Giáo dục: *Lớp AI/CNTT, Phòng Đào tạo, Khoa Kinh tế, CTSV, Thư viện*; Y tế: *Khoa Khám bệnh, Khoa Dược, Hành chính*) và cho phép tự nhập tên Đơn vị/Lớp học mới (`__CUSTOM__`).
* **`FR-05` (Client-side PDF Extraction & Paragraph Chunking):** Trích xuất trực tiếp nội dung file `.pdf` nhiều trang trên trình duyệt bằng **Mozilla PDF.js**, làm sạch UTF-8, phân mảnh theo khối đoạn văn (`\n\n`, lọc bỏ đoạn nhiễu $\le 25$ ký tự, giới hạn $2.000$ ký tự/chunk khi gọi API) và nhúng thành Vector **3.072 chiều** qua `models/gemini-embedding-001`.
* **`FR-06` (Live Playground & Trace Stream):** Kiểm thử trực tiếp Agent ngay trong Studio với cửa sổ hiển thị luồng suy luận (`Intent` $\rightarrow$ `Latency` $\rightarrow$ `Citation Source`).

### 4.3. Phân hệ AI Engine & Luồng Phê duyệt HITL (`FR-07` -> `FR-10`)
* **`FR-07` (Unit ACL Runtime Guardrail):** Kiểm tra xác thực người dùng và đối chiếu cứng `user.department == agent.department_access` ngay tại cổng API `/api/chat` trước khi gọi LLM (không fallback sang tài khoản hoặc tổ chức khác).
* **`FR-08` (StateGraph Intent Routing):** `LangGraphAgent` phân loại luồng tin nhắn tại **Node 1** giữa khởi tạo đề xuất nghiệp vụ (`CREATE_REQUEST`) và tra cứu tri thức (`RAG_SEARCH`).
* **`FR-09` (Pre-filtered Vector Search & Citation Grounding):** Tại **Node 2**, hệ thống tiền lọc vector theo cả **Lớp 1 (`tenant_id`)** và **Lớp 2 (`department_access`)** trong `backend/vector_store.py`, chấm điểm **Cosine Similarity** (ngưỡng $> 0.35$), sinh câu trả lời bằng `gemini-flash-latest` (`temperature = 0.2`) và bắt buộc đính kèm hộp **Nguồn trích dẫn (Citation Box)**.
* **`FR-10` (Human-in-the-Loop Approval Workflow):** Khi phát hiện ý định trình ký/đề xuất, hệ thống tạm dừng (`interrupt_hitl = True`) để người dùng bấm xác nhận, lưu bản ghi `PENDING` vào CSDL, hiển thị trên hộp thư của `TENANT_ADMIN` và đẩy thông báo Toast thời gian thực về màn hình người gửi ngay khi được duyệt.

---

## 5. Kiến trúc Dữ liệu & Danh mục API (Data Schema & API Endpoints)

### 5.1. Cấu trúc 5 Bảng CSDL Quan hệ (`SQLite 3` & `MySQL 8.0`)
1. **`tenants`**: `id (PK)`, `name`, `contact_email`, `plan_type`, `domain_type`, `ui_schema`, `max_agents`, `max_employees`, `is_active`, `created_at`.
2. **`users`**: `id (PK)`, `tenant_id (FK)`, `email`, `hashed_password`, `full_name`, `department` *(Đơn vị/Phòng ban/Lớp)*, `role`, `tenure_months`, `total_leave_days`, `used_leave_days`, `attributes`, `is_active`, `created_at`.
3. **`agents`**: `id (PK)`, `tenant_id (FK)`, `name`, `description`, `instruction` *(System Prompt)*, `department_access` *(Phạm vi ACL)*, `is_published`, `creator_id`, `created_at`.
4. **`documents`**: `id (PK)`, `tenant_id (FK)`, `file_name`, `file_path`, `file_size_kb`, `uploaded_at`.
5. **`leave_requests` (HITL Requests)**: `id (PK)`, `tenant_id (FK)`, `user_id`, `user_name`, `days_requested` *(Số lượng/Định mức)*, `date_details` *(Nội dung đề xuất)*, `status` (`PENDING` / `APPROVED` / `REJECTED`), `notified_to_user`, `created_at`.

### 5.2. Danh mục RESTful API chính (`backend/server.py`)
* `GET / POST /api/tenants`, `GET / POST /api/tenants/ui_schema`, `POST /api/tenants/generate_schema`, `POST /api/tenants/delete`: Quản lý Tổ chức & Động cơ UI Schema đa ngành.
* `GET / POST /api/users`, `GET /api/users/<id_or_email>`, `POST /api/users/bulk`, `POST /api/users/update`, `POST /api/users/delete`: Quản lý Thành viên & Đơn vị + Đồng bộ Keycloak & SMTP.
* `GET / POST /api/agents`: Danh sách & Xuất bản Agent theo `tenant_id` và `department_access`.
* `GET / POST /api/documents`: Lưu trữ tài liệu & kích hoạt Vector hóa 3.072 chiều.
* `POST /api/chat`: Cổng điều phối `LangGraphAgent` (Identity & Unit ACL Check $\rightarrow$ Node 1: Intent/HITL $\rightarrow$ Node 2: Pre-filtered Vector RAG + Gemini LLM).
* `GET / POST /api/leave_requests`, `POST /api/leave_requests/decision`, `GET /api/notifications`: Luồng trình ký & thông báo duyệt HITL thời gian thực.

---

## 6. Yêu cầu Phi chức năng (NFRs)

* **Hiệu năng (Latency):** Thời gian phản hồi trung bình cho truy vấn RAG $< 3.0\text{ giây}$; thời gian chặn truy cập trái phép (`ACL_DENIED`) $< 0.05\text{ giây}$.
* **Bảo mật & Cô lập dữ liệu (Zero Data Leakage):** $0\%$ rò rỉ tài liệu giữa các `tenant_id` khác nhau hoặc giữa các `department` không được cấp quyền nhờ cơ chế Pre-retrieval Filtering ở cả API và Vector Store.

---

## 7. Bảng Đối chiếu Thực tế Triển khai: Bản MVP (Demo 1) vs. Lộ trình Nâng cấp (Phase 2 Roadmap)

Để đảm bảo tính minh bạch kỹ thuật khi nghiệm thu Demo 1, bảng dưới đây phân định rõ các hạng mục **đã chạy hoàn chỉnh trong codebase hiện tại** và các hạng mục **định hướng mở rộng ở Phase 2** (như đề cập trong tầm nhìn của `Brief.md`):

| Hạng mục Kỹ thuật | Đã triển khai hoàn chỉnh trong Bản MVP (Demo 1) | Lộ trình Nâng cấp ở Phase 2 (Production Roadmap) |
| :--- | :--- | :--- |
| **1. Backend & CSDL** | Python `ThreadingHTTPServer` (`backend/server.py`), CSDL `SQLite 3` (`database.db`) & bản xuất `MySQL 8.0`. | Chuyển đổi sang `FastAPI` + `PostgreSQL` bất đồng bộ chịu tải cao. |
| **2. Điều phối Agent (Orchestration)** | Lớp `LangGraphAgent` tự xây dựng (`backend/agent_engine.py`) gồm **2 Node chính** (Node 1: Intent & HITL Interrupt; Node 2: Pre-filtered Vector RAG & Gemini LLM). | Nâng cấp lên thư viện `langgraph.graph.StateGraph` đa node kèm `MemorySaver` Checkpoint bền vững. |
| **3. Chiến lược Chunking & Vector DB** | Bóc tách PDF qua `PDF.js`, chia theo đoạn văn `\n\n` (`len > 25`), lưu JSON Vector 3.072 chiều (`gemini-embedding-001`) kèm bộ lọc trước (`Pre-filtering`) theo `tenant_id` và `department`. | Áp dụng **Recursive Character Text Splitter** (`chunk_size = 500`, `overlap = 100`), gắn thẻ cấu trúc Điều/Khoản và lưu trên máy chủ Vector `Qdrant`. |
| **4. Xác thực & Bảo mật Mật khẩu** | Xác thực OIDC tập trung 100% qua **Keycloak SSO** (mật khẩu được băm PBKDF2/Argon2 bên trong Keycloak). | Băm `bcrypt` cho toàn bộ cột `hashed_password` trong bảng `users` nội bộ và xác thực chữ ký JWT trực tiếp tại Backend middleware. |
| **5. Giám sát (Observability) & Context Core** | Đo lường trực tiếp `latency`, `token_estimate`, `intent`, `citation` trả về Live Playground Trace (`#traceLogContent`) và Dashboard thống kê (`#tab-analytics`). | Tích hợp trực tiếp `langfuse` Python SDK và hoàn thiện module tách luồng hội thoại nhóm đan xen (*Thread Disentanglement* & *Temporal State Tracking*). |
