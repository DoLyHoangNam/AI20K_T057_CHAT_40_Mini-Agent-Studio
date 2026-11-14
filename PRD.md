# PRODUCT REQUIREMENTS DOCUMENT (PRD) — MINI AGENT STUDIO (CHAT-40)

* **Tên sản phẩm:** Mini Agent Studio — Nền tảng No-Code khởi tạo AI Agent đa lĩnh vực, xử lý đan xen hội thoại & phân quyền theo đơn vị
* **Mã đề tài:** CHAT-40 | **Đội ngũ phát triển:** AI20K - Team T057
* **Phiên bản:** v2.0 | **Trạng thái:** Ready for Review

---

## 1. Tóm tắt Điều hành (Executive Summary)

**Mini Agent Studio (CHAT-40)** là nền tảng SaaS Multi-Tenant & Multi-Domain cho phép Quản trị viên của bất kỳ tổ chức nào (**Doanh nghiệp, Trường học, Bệnh viện, Tổ chức**) tự khởi tạo, cấu hình và phân quyền các **Trợ lý AI chuyên biệt theo từng Đơn vị (`department`)** mà không cần viết code:
* **Khối Doanh nghiệp:** Chia theo Phòng ban (*Marketing, Kế toán - Tài chính, Nhân sự - HR, Kỹ thuật - IT, Kinh doanh - Sales...*).
* **Khối Giáo dục:** Chia theo Khoa / Lớp học / Phòng chức năng (*Lớp AI - K68, Khoa CNTT, Khoa Kinh tế, Phòng Đào tạo, Công tác Sinh viên, Thư viện...*).
* **Khối Y tế & Tổ chức:** Chia theo Chuyên khoa / Bộ phận (*Khoa Khám bệnh, Khoa Dược, Hành chính viện...*).

Bên cạnh giao diện **No-Code Studio Builder**, nền tảng giải quyết 3 bài toán kỹ thuật cốt lõi trong môi trường hội thoại thực tế:
1. **Tách luồng hội thoại đan xen (Thread Disentanglement)** & **Theo dõi trạng thái thời gian (Temporal State Tracking)**.
2. **Cô lập dữ liệu đa tầng (3-Layer RBAC & Unit ACL)** trên kho tri thức Vector 3.072 chiều (`gemini-embedding-001`).
3. **Trích dẫn nguồn chính xác (Citation Grounding)** & **Trạm phê duyệt con người (Human-in-the-Loop - HITL)**.

---

## 2. Chân dung Người dùng & Bài toán (User Personas & Use Cases)

| Nhóm người dùng | Mã Vai trò (`role`) | Đặc điểm & Nhu cầu cốt lõi |
| :--- | :--- | :--- |
| **1. Chủ nền tảng (Platform Owner)** | `SUPER_ADMIN` | Cấp bản quyền, khởi tạo không gian làm việc độc lập (`Tenant`) cho các Doanh nghiệp/Trường học mới, quản lý tài khoản toàn hệ thống và giám sát CSDL. |
| **2. Quản trị Tổ chức / Trưởng bộ phận / Giáo vụ** | `TENANT_ADMIN` | Không chuyên lập trình nhưng cần tạo nhanh các Agent theo từng Phòng ban / Khoa / Lớp học (qua 1-Click Templates hoặc tùy chỉnh), tải lên tài liệu PDF/TXT nội bộ, nhập danh sách thành viên (CSV) và phê duyệt các đề xuất phát sinh từ luồng **HITL**. |
| **3. Thành viên / Nhân viên / Sinh viên** | `EMPLOYEE` | Truy cập cổng Chat để hỏi đáp quy chế, tài liệu chuyên môn hoặc bài giảng của đúng đơn vị mình (có trích dẫn nguồn), đồng thời gửi các đề xuất/đơn từ nghiệp vụ trình cấp quản lý phê duyệt. |

---

## 3. Ma trận Phân quyền Đa tầng (3-Layer RBAC & Unit ACL Matrix)

Mỗi người dùng được định danh bởi bộ 3 khóa: `tenant_id` (Tổ chức), `role` (Vai trò) và `department` (Đơn vị: Phòng ban / Khoa / Lớp học).

| Chức năng / Tài nguyên | `SUPER_ADMIN` | `TENANT_ADMIN` | `EMPLOYEE` (Thành viên đơn vị) |
| :--- | :---: | :---: | :---: |
| Khởi tạo / Xóa Tổ chức (`Tenants`) | ✅ Toàn quyền | ❌ | ❌ |
| Truy cập Studio Builder & Tạo Agent mới | ✅ | ✅ (Trong `tenant_id`) | ❌ (Chặn bởi Route Guard) |
| Tải tài liệu PDF/TXT & Vector hóa 3072-dim | ✅ | ✅ (Trong `tenant_id`) | ❌ |
| Thêm / Sửa / Xóa Thành viên & Nhập CSV | ✅ (Toàn hệ thống) | ✅ (Trong `tenant_id`) | ❌ |
| Chat với Agent toàn tổ chức (`department_access = ALL`) | ✅ | ✅ | ✅ |
| Chat với Agent chuyên biệt (`department_access = X`) | ✅ | ✅ | ✅ **Chỉ khi `user.department == X`**<br>*(Ngược lại bị chặn `ACL_DENIED`)* |
| Khởi tạo đề xuất / yêu cầu phê duyệt (`HITL Request`) | ✅ | ✅ | ✅ (Trạng thái `PENDING`) |
| Phê duyệt / Từ chối đề xuất (`APPROVED` / `REJECTED`) | ✅ | ✅ (Approver) | ❌ |

---

## 4. Yêu cầu Chức năng (Functional Requirements)

### 4.1. Phân hệ Quản trị Nền tảng & Định danh SSO (`FR-01` -> `FR-03`)
* **`FR-01` (Keycloak OIDC SSO):** Xác thực tập trung qua Keycloak Server (`http://localhost:8080`, Realm `mini-agent-platform`), tự động điều hướng theo `role`.
* **`FR-02` (Multi-Tenant Provisioning):** `SUPER_ADMIN` khởi tạo tổ chức mới theo lĩnh vực (`ENTERPRISE`, `EDUCATION`, `HEALTHCARE`, `CUSTOM`), hệ thống tự động sinh tài khoản `TENANT_ADMIN` đầu tiên, đồng bộ lên Keycloak và gửi email bàn giao mật khẩu qua SMTP.
* **`FR-03` (Bulk Member Provisioning):** `TENANT_ADMIN` thêm thành viên đơn lẻ hoặc tải file CSV/TXT hàng loạt (`Họ tên, Email, Đơn vị`), tự động gán quyền truy cập theo đơn vị.

### 4.2. Phân hệ No-Code Studio Builder & Kho Tri thức RAG (`FR-04` -> `FR-06`)
* **`FR-04` (Multi-Industry Agent Templates):** Cung cấp 13+ mẫu Agent dựng sẵn cho 3 nhóm ngành (Doanh nghiệp: *Marketing, Kế toán, HR, IT, Sales*; Giáo dục: *Lớp AI/CNTT, Phòng Đào tạo, Khoa Kinh tế, CTSV, Thư viện*; Y tế: *Khoa Khám bệnh, Khoa Dược, Hành chính*) và cho phép tự nhập tên Đơn vị/Lớp học mới (`__CUSTOM__`).
* **`FR-05` (Client-side PDF Extraction & Semantic Chunking):** Trích xuất trực tiếp nội dung file `.pdf` nhiều trang bằng **Mozilla PDF.js**, làm sạch UTF-8, phân mảnh theo khối đoạn văn ngữ nghĩa (`\n\n`, lọc đoạn $> 25$ ký tự, giới hạn $2.000$ ký tự) và nhúng thành Vector **3.072 chiều** qua `gemini-embedding-001`.
* **`FR-06` (Live Playground & Trace Stream):** Kiểm thử trực tiếp Agent ngay trong Studio với cửa sổ hiển thị luồng suy luận (`Intent` $\rightarrow$ `Latency` $\rightarrow$ `Citation Source`).

### 4.3. Phân hệ AI Context Core & Luồng Phê duyệt HITL (`FR-07` -> `FR-10`)
* **`FR-07` (Unit ACL Runtime Guardrail):** Kiểm tra quyền `user.department == agent.department_access` ngay tại cổng API `/api/chat` trước khi gọi LLM.
* **`FR-08` (Intent Routing & Thread Handling):** Tự động phân loại luồng tin nhắn giữa tra cứu tri thức (`RAG_SEARCH`) và khởi tạo đề xuất nghiệp vụ (`CREATE_REQUEST`), xử lý ngữ cảnh hội thoại đan xen và ưu tiên trạng thái thông tin mới nhất theo thời gian.
* **`FR-09` (Pre-filtered Vector Search & Citation Grounding):** Tiền lọc vector theo `tenant_id`, chấm điểm **Cosine Similarity** (ngưỡng $> 0.35$), sinh câu trả lời bằng `gemini-flash-latest` (`temperature = 0.2`) và bắt buộc đính kèm hộp **Nguồn trích dẫn (Citation Box)**.
* **`FR-10` (Human-in-the-Loop Approval Workflow):** Khi phát hiện ý định trình ký/đề xuất, hệ thống tạm dừng để người dùng bấm xác nhận, lưu bản ghi `PENDING` vào CSDL, hiển thị trên hộp thư của `TENANT_ADMIN` và đẩy thông báo Toast thời gian thực về màn hình người gửi ngay khi được duyệt.

---

## 5. Kiến trúc Dữ liệu & Danh mục API (Data Schema & API Endpoints)

### 5.1. Cấu trúc 5 Bảng CSDL Quan hệ (`SQLite 3` & `MySQL 8.0`)
1. **`tenants`**: `id (PK)`, `name`, `contact_email`, `plan_type`, `domain_type`, `ui_schema`, `created_at`.
2. **`users`**: `id (PK)`, `tenant_id (FK)`, `email`, `hashed_password`, `full_name`, `department` *(Đơn vị/Phòng ban/Lớp)*, `role`, `attributes`.
3. **`agents`**: `id (PK)`, `tenant_id (FK)`, `name`, `description`, `instruction` *(System Prompt)*, `department_access` *(Phạm vi ACL)*.
4. **`documents`**: `id (PK)`, `tenant_id (FK)`, `file_name`, `file_path`, `file_size_kb`, `uploaded_at`.
5. **`leave_requests` (HITL Requests)**: `id (PK)`, `tenant_id (FK)`, `user_id`, `user_name`, `days_requested` *(Số lượng/Định mức)*, `date_details` *(Nội dung đề xuất)*, `status` (`PENDING` / `APPROVED` / `REJECTED`), `notified_to_user`.

### 5.2. Danh mục RESTful API chính (`backend/server.py`)
* `GET / POST /api/tenants` & `POST /api/tenants/delete`: Quản lý Tổ chức (Super Admin).
* `GET / POST /api/users`, `POST /api/users/bulk`, `POST /api/users/update`, `POST /api/users/delete`: Quản lý Thành viên & Đơn vị + Đồng bộ Keycloak.
* `GET / POST /api/agents`: Danh sách & Xuất bản Agent theo `tenant_id` và `department_access`.
* `GET / POST /api/documents`: Quản lý tài liệu & kích hoạt Vector hóa 3.072 chiều.
* `POST /api/chat`: Cổng điều phối LangGraph State Engine (ACL Check $\rightarrow$ Intent Router $\rightarrow$ Vector RAG / HITL).
* `GET / POST /api/leave_requests`, `POST /api/leave_requests/decision`, `GET /api/notifications`: Luồng trình ký & thông báo duyệt HITL thời gian thực.

---

## 6. Yêu cầu Phi chức năng & Chỉ số Đánh giá (NFRs & Evaluation Metrics)

* **Hiệu năng (Latency):** Thời gian phản hồi trung bình (P95) cho truy vấn RAG $< 3.0\text{ giây}$; thời gian chặn truy cập trái phép (`ACL_DENIED`) $< 0.05\text{ giây}$.
* **Bảo mật & Cô lập dữ liệu (Zero Data Leakage):** $0\%$ rò rỉ tài liệu giữa các `tenant_id` khác nhau hoặc giữa các `department` không được cấp quyền.
* **Chất lượng AI (Evaluation KPIs):**
  * Độ chính xác tách luồng hội thoại (*Thread Disentanglement*): $\text{Micro-F1} \ge 0.72$.
  * Phát hiện trạng thái bị ghi đè (*Temporal State Tracking*): $\ge 80\%$.
  * Độ trung thực trích dẫn nguồn (*Citation Faithfulness*): $\ge 90\%$.
