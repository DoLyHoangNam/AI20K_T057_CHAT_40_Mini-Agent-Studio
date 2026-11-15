# PRODUCT REQUIREMENTS DOCUMENT (PRD) — MINI AGENT STUDIO (CHAT-40)

* **Tên sản phẩm:** Mini Agent Studio — Nền tảng No-Code khởi tạo AI Agent cho mọi Công ty & Tổ chức, xử lý đan xen hội thoại nhóm & phân quyền cô lập theo đơn vị
* **Mã đề tài:** CHAT-40 | **Đội ngũ phát triển:** AI20K - Team T057
* **Phiên bản:** v3.0 (Đồng bộ 100% với `Brief.md`, `Wireframe_UI_Flow.md` & Codebase Thực tế) | **Trạng thái:** Ready for Review

---

## 1. Mục tiêu Sản phẩm (Product Objectives & Universal Positioning)

### 1.1. Định vị Sản phẩm: Nền tảng AI Agent cho BẤT KỲ Công ty & Tổ chức nào
**Mini Agent Studio (CHAT-40)** là nền tảng SaaS Multi-Tenant cho phép Quản trị viên của **bất kỳ công ty hay tổ chức nào** (Công nghệ, Tài chính - Ngân hàng, Sản xuất, Bán lẻ, Logistics, Dịch vụ, Giáo dục, Y tế...) tự khởi tạo, cấu hình và phân quyền các **Trợ lý AI chuyên biệt theo từng Đơn vị vận hành (`department`)** chỉ trong vài phút mà không cần viết code.

Để đảm bảo bất kỳ công ty nào khi áp dụng hệ thống cũng tương thích ngay lập tức mà không cần sửa đổi kiến trúc lõi, hệ thống chuẩn hóa mọi mô hình tổ chức về **4 thực thể trừu tượng** và tự động biến đổi giao diện thông qua **Adaptive UI Schema Engine (`backend/schema_engine.py`)**:

| Khái niệm Lõi (`Core Abstraction`) | Kịch bản Trọng tâm: Mọi Công ty & Doanh nghiệp (`ENTERPRISE` — Công nghệ, Ngân hàng, Sản xuất, Bán lẻ, Logistics...) | Ví dụ Mở rộng 1: Giáo dục & Đào tạo (`EDUCATION`) | Ví dụ Mở rộng 2: Y tế & Bệnh viện (`HEALTHCARE`) | Ví dụ Mở rộng 3: Ngành nghề Bất kỳ Khác (`CUSTOM` — AI Auto-Schema) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Tổ chức (`tenant_id`)** | Công ty / Tập đoàn (VD: `VINFAST`, `FPT`, Ngân hàng, Chuỗi bán lẻ...) | Trường Đại học / Học viện (VD: `VNU` - ĐHQG) | Bệnh viện / Phòng khám (VD: `BVQT`) | Công ty Luật, Logistics, Bất động sản, NGO... |
| **2. Đơn vị (`department`)** | Phòng ban / Chi nhánh / Dự án (*Marketing, Kế toán - Tài chính, Nhân sự - HR, Kỹ thuật - IT, Kinh doanh - Sales...*) | Khoa / Viện / Lớp học / Phòng chức năng (*Phòng Đào tạo, Khoa CNTT, Lớp AI - K68, CTSV...*) | Chuyên khoa / Bộ phận (*Khoa Nội, Khoa Khám bệnh, Khoa Dược, Hành chính...*) | Ban chuyên môn / Đội vận hành / Chi nhánh vùng |
| **3. Thành viên (`role`)** | Quản trị công ty / Trưởng phòng (`TENANT_ADMIN`), Nhân viên (`EMPLOYEE`) | Giáo vụ / Chủ nhiệm khoa (`TENANT_ADMIN`), Sinh viên / Giảng viên (`EMPLOYEE`) | Quản lý viện / Trưởng khoa (`TENANT_ADMIN`), Bác sĩ / Điều dưỡng (`EMPLOYEE`) | Trưởng bộ phận (`TENANT_ADMIN`), Chuyên viên (`EMPLOYEE`) |
| **4. Luồng Phê duyệt (`HITL`)** | Duyệt ngân sách chiến dịch, xin nghỉ phép, mua sắm thiết bị, duyệt hợp đồng | Xin hoãn thi, đăng ký học phần, mượn phòng Lab, duyệt đề tài | Duyệt cấp phát thuốc đặc trị, đề xuất hội chẩn liên khoa | Phê duyệt hồ sơ pháp lý, lệnh điều xe, giải ngân |

> **Định hướng trọng tâm trong tài liệu:** Toàn bộ quy trình nghiệp vụ dưới đây lấy **Khối Doanh nghiệp / Công ty (`ENTERPRISE`)** làm kịch bản chính để mô tả sâu. Các lĩnh vực **Giáo dục (`EDUCATION`)**, **Y tế (`HEALTHCARE`)** và **Tùy chỉnh (`CUSTOM`)** đóng vai trò là các preset mở rộng chứng minh tính linh hoạt đa ngành của nền tảng.

---

### 1.2. Bốn Mục tiêu Cốt lõi của Sản phẩm
1. **Dân chủ hóa việc tạo AI Agent theo Phòng ban (No-Code Time-to-Value $< 3\text{ phút}$):** Giúp các Trưởng phòng nghiệp vụ (Marketing, Kế toán, HR, IT, Sales...) tự khởi tạo Agent, nạp tài liệu PDF quy chế nội bộ, gắn công cụ (Tools) và thiết lập luồng xử lý thông qua giao diện kéo thả mà không phụ thuộc vào đội ngũ lập trình viên.
2. **Cô lập Dữ liệu Đa tầng Tuyệt đối (100% Tenant & Unit ACL Isolation):** Đảm bảo nhân viên thuộc phòng ban nào chỉ được phép truy xuất tri thức và tương tác với Agent của phòng ban đó (hoặc Agent chung toàn công ty `ALL`). Triệt tiêu 100% nguy cơ lộ lọt tài liệu nhạy cảm giữa các phòng ban và giữa các công ty thông qua cơ chế **Pre-retrieval Vector Filtering** ngay tại tầng lưu trữ.
3. **Giải quyết Hỗn loạn Ngữ cảnh trong Hội thoại Nhóm (Group Chat Context Core):** Xử lý hiệu quả bài toán nhiều thành viên trao đổi đan xen đa chủ đề (**Thread Disentanglement**), tự động loại bỏ các quyết định/lịch hẹn cũ đã bị thay thế theo thời gian (**Temporal State Tracking: `ACTIVE` vs. `OVERRIDDEN`**) và bắt buộc trích dẫn bằng chứng nguồn 2 chiều (**Citation Grounding: `#msg_id` & Document Chunk**).
4. **Kiểm soát Rủi ro Thực thi bằng Con người (100% HITL Governance):** Mọi hành động nhạy cảm hoặc làm thay đổi dữ liệu nghiệp vụ (tạo đề xuất ngân sách, nộp đơn nghỉ phép, gửi thông báo...) đều bắt buộc đi qua trạm dừng **Human-in-the-Loop (HITL Interrupt)** để Trưởng phòng/Quản trị viên phê duyệt trước khi có hiệu lực.

---

## 2. Phạm vi Sản phẩm (Product Scope — In-Scope vs. Out-of-Scope)

Để đồng bộ tuyệt đối giữa **tầm nhìn sản phẩm CHAT-40** và **trạng thái mã nguồn thực tế**, mọi tính năng trong PRD được gắn nhãn theo 3 mức:
- `✅ Đã có trong bản dựng hiện tại (Implemented in Prototype)`: Đã chạy thực tế end-to-end trong codebase hiện tại.
- `🛠 Cam kết hoàn thiện trong MVP (MVP Target Scope)`: Nằm trong phạm vi bắt buộc của đề tài CHAT-40, đã chuẩn hóa thiết kế và hoàn thiện trong chu kỳ MVP.
- `🚀 Lộ trình Mở rộng Nâng cao (Phase 2 / P1)`: Các tính năng nâng cao phát triển sau MVP.

### 2.1. Trong phạm vi MVP (In-Scope)
- **Phân hệ Quản trị Đa Tổ chức & Định danh SSO:**
  - `✅` Xác thực tập trung qua **Keycloak OIDC/OAuth2 SSO** (`http://localhost:8080`, Realm `mini-agent-platform`) và tự động cấp phát mật khẩu qua **Google Gmail SMTP** (`backend/mailer.py`).
  - `✅` Khởi tạo công ty mới (`Tenant Provisioning`) kèm **Adaptive UI Schema Engine** (`backend/schema_engine.py`) hỗ trợ mọi ngành nghề công ty (`ENTERPRISE`, `EDUCATION`, `HEALTHCARE`, `CUSTOM`).
  - `✅` Quản lý nhân sự theo phòng ban/đơn vị, hỗ trợ thêm lẻ và nhập hàng loạt qua file CSV/TXT.
- **Phân hệ No-Code Studio Builder & Kho Tri thức Vector RAG:**
  - `✅` Khởi tạo Agent qua 13+ mẫu dựng sẵn hoặc tự định nghĩa phòng ban mới (`__CUSTOM__`); bóc tách PDF nhiều trang ngay trên trình duyệt (`Mozilla PDF.js`), phân mảnh đoạn văn và nhúng Vector **3.072 chiều** (`models/gemini-embedding-001`) kèm **Pre-filtering ACL**.
  - `🛠` Trình kéo thả **Workflow 3–5 Node (React Flow)**, tích hợp **$\ge 3$ MCP-like Tools** (`leave_balance`, `leave_request_create`, `send_email`) kèm **Permission Manifest**, bộ nhớ hội thoại (**Basic Memory**) và quản lý phiên bản bất biến (**Agent Versioning `v1.0`, `v1.1`**).
- **Phân hệ AI Context Core (Chat 1-1 & Group Chat) & Luồng Duyệt HITL:**
  - `✅` **Luồng Phê duyệt Con người (HITL Interrupt):** Tự động chặn các yêu cầu trình ký/đề xuất, lưu trạng thái `PENDING`, hiển thị trên hộp thư Admin và đẩy thông báo Toast thời gian thực khi được duyệt (`APPROVED` / `REJECTED`).
  - `🛠` **Group Chat Sandbox (Role Switcher) + Tách luồng hội thoại đan xen (Thread Disentanglement) + Theo dõi trạng thái quyết định theo thời gian (Temporal State Tracking `ACTIVE`/`OVERRIDDEN`/`CANCELLED`/`DONE`) + Trích dẫn 2 chiều (`#msg_id` & Document Citation Box)**.
- **Phân hệ Lưu trữ Kép & Giám sát (Observability):**
  - `✅` CSDL `SQLite 3` nội bộ đồng bộ thời gian thực (`AutoSyncSQLiteConnection` trong `backend/mysql_sync.py`) sang **MySQL 8.0 Server** để kiểm tra trực quan trên **MySQL Workbench 8.0 CE**; kèm **X-Ray Telemetry Trace** trên giao diện.
  - `🛠` Tích hợp trực tiếp **Langfuse SDK** và bộ kịch bản đánh giá tự động (Evaluation Benchmark Pipeline).

### 2.2. Ngoài phạm vi MVP (Out-of-Scope)
- **Không** xây dựng cổng thanh toán trực tuyến (Billing/Subscription) hoặc chợ giao dịch Agent công cộng (Public Marketplace).
- **Không** tích hợp webhook trực tiếp vào các nền tảng chat bên thứ ba (Zalo, Slack, Microsoft Teams, Discord) trong giai đoạn MVP — toàn bộ trải nghiệm Chat 1-1 và Group Chat được thực hiện trên Web Portal nội bộ.
- **Không** tự huấn luyện (pre-train) hoặc fine-tune mô hình ngôn ngữ lớn; không xử lý dữ liệu âm thanh/video thời gian thực.

---

## 3. Đối tượng Người dùng & Ma trận Phân quyền (Target Users & RBAC/ACL Matrix)

### 3.1. Chân dung 3 Nhóm Người dùng (User Personas)

| Nhóm người dùng | Mã Vai trò (`role`) | Đặc điểm, Quyền hạn & Nhu cầu cốt lõi |
| :--- | :--- | :--- |
| **1. Chủ nền tảng (Platform Owner)** | `SUPER_ADMIN` | Đội ngũ vận hành SaaS. Cấp bản quyền, khởi tạo không gian làm việc độc lập (`Tenant`) cho các Công ty/Tổ chức mới, chọn lĩnh vực hoạt động (hoặc dùng AI sinh Schema cho ngành nghề mới), tự động đồng bộ tài khoản lên Keycloak SSO và gửi email bàn giao qua Gmail SMTP. |
| **2. Quản trị Công ty / Trưởng Phòng ban** | `TENANT_ADMIN` | Giám đốc vận hành, Trưởng phòng HR/Marketing/Kế toán/IT (hoặc Giáo vụ/Trưởng khoa ở kịch bản mở rộng). Không chuyên lập trình nhưng cần tạo nhanh Agent cho từng phòng ban, upload tài liệu PDF/TXT nội bộ, cấu hình Tool & Workflow, nhập danh sách nhân sự (CSV) và **phê duyệt các đề xuất phát sinh từ luồng HITL**. |
| **3. Nhân viên / Thành viên Đơn vị** | `EMPLOYEE` | Nhân viên thuộc một phòng ban cụ thể trong công ty. Truy cập cổng Chat để hỏi đáp quy chế/tài liệu của đúng phòng ban mình (Chat 1-1), thảo luận công việc đa luồng cùng đồng nghiệp có `@Agent` hỗ trợ (Group Chat), và gửi đề xuất/đơn từ trình cấp quản lý phê duyệt. |

---

### 3.2. Kịch bản Sử dụng Thực tế: Khi nào dùng Chat 1-1 vs. Khi nào dùng Chat Nhóm?
- **Kịch bản A — Chat 1-1 (`Direct 1-1 Assistant`):** Dùng khi nhân viên cần hỏi đáp thông tin quy chế liên quan đến cá nhân hoặc thực hiện tác vụ trình ký riêng lẻ (Ví dụ: *"Kiểm tra giúp tôi còn bao nhiêu ngày phép?"*, *"Quy trình hoàn ứng chi phí tiếp khách của Phòng Marketing cần những chứng từ gì?"*, *"Tạo đề xuất duyệt ngân sách chạy quảng cáo TikTok 50 triệu"*).
- **Kịch bản B — Chat Nhóm Phòng ban (`Multi-User Group Chat Sandbox`):** Dùng khi 3–5 thành viên trong cùng phòng ban/dự án cùng trao đổi đan xen nhiều đầu việc trên một kênh chung (Ví dụ: vừa bàn nội dung sự kiện ra mắt sản phẩm, vừa thay đổi lịch họp từ Thứ Ba sang Thứ Năm, vừa chốt lại người phụ trách). Khi một thành viên gõ `@Agent tóm tắt các quyết định mới nhất đang có hiệu lực của từng đầu việc`, Agent sẽ tách riêng từng luồng chủ đề, bỏ qua các lịch hẹn cũ đã bị ghi đè (`OVERRIDDEN`), chỉ tổng hợp các quyết định đang `ACTIVE` và gắn kèm mã tin nhắn `#msg_id` làm bằng chứng.

---

### 3.3. Ma trận Phân quyền Đa tầng (3-Layer RBAC & Unit ACL Matrix)
Mỗi người dùng được định danh chặt chẽ bởi bộ 3 khóa: `tenant_id` (Công ty/Tổ chức), `role` (Vai trò hệ thống) và `department` (Đơn vị/Phòng ban).

| Chức năng / Tài nguyên Hệ thống | `SUPER_ADMIN` | `TENANT_ADMIN` | `EMPLOYEE` (Thành viên đơn vị) |
| :--- | :---: | :---: | :---: |
| Khởi tạo / Xóa Công ty (`Tenants`) & Sinh `ui_schema` | ✅ Toàn quyền | ❌ | ❌ |
| Truy cập No-Code Studio Builder & Tạo/Xuất bản Agent | ✅ | ✅ (Trong `tenant_id`) | ❌ (Chặn bởi Route Guard) |
| Tải tài liệu PDF/TXT & Vector hóa 3.072 chiều | ✅ | ✅ (Trong `tenant_id`) | ❌ |
| Thêm / Sửa / Xóa Thành viên & Nhập CSV hàng loạt | ✅ (Toàn hệ thống) | ✅ (Trong `tenant_id`) | ❌ |
| Chat với Agent toàn công ty (`department_access = ALL`) | ✅ | ✅ | ✅ (Chỉ truy xuất tài liệu `ALL` của đúng `tenant_id`) |
| Chat với Agent chuyên biệt (`department_access = X`) | ✅ | ✅ | ✅ **Chỉ khi `user.department == X`**<br>*(Ngược lại bị chặn cứng `ACL_DENIED`)* |
| Khởi tạo đề xuất / yêu cầu phê duyệt (`HITL Request`) | ✅ | ✅ | ✅ (Khởi tạo ở trạng thái `PENDING`) |
| Phê duyệt / Từ chối đề xuất (`APPROVED` / `REJECTED`) | ✅ | ✅ (Approver) | ❌ (Chỉ nhận thông báo kết quả) |

---

## 4. Yêu cầu Chức năng (Functional Requirements)

### 4.1. Phân hệ Quản trị Nền tảng, Đa Ngành nghề & Định danh SSO (`FR-01` → `FR-03`)
* **`FR-01` (Keycloak OIDC SSO Authentication) [`✅`]:** Xác thực tập trung 100% qua máy chủ Keycloak (`http://localhost:8080`, Realm `mini-agent-platform`), tự động ánh xạ danh tính từ OIDC Token sang hồ sơ người dùng nội bộ và điều hướng giao diện theo `role`.
* **`FR-02` (Universal Tenant Provisioning & Adaptive UI Schema) [`✅`]:** `SUPER_ADMIN` khởi tạo công ty/tổ chức mới với lựa chọn ngành nghề (`ENTERPRISE` làm mặc định cho mọi doanh nghiệp, cùng các mẫu mở rộng `EDUCATION`, `HEALTHCARE` hoặc nhập mô tả tự do `CUSTOM` để AI tự sinh `ui_schema` qua `backend/schema_engine.py`). Hệ thống tự động tạo tài khoản `TENANT_ADMIN`, đồng bộ lên Keycloak và gửi mật khẩu ngẫu nhiên qua Gmail SMTP (`backend/mailer.py`).
* **`FR-03` (Bulk Unit Member Provisioning) [`✅`]:** `TENANT_ADMIN` thêm nhân sự đơn lẻ hoặc tải lên file CSV/TXT hàng loạt (`Họ tên, Email, Phòng ban/Đơn vị`), hệ thống tự động gán quyền ACL theo đơn vị và cấp tài khoản SSO.

### 4.2. Phân hệ No-Code Studio Builder, Workflow & Kho Tri thức RAG (`FR-04` → `FR-07`)
* **`FR-04` (Multi-Unit Agent Templates & Custom Department Creation) [`✅`]:** Cung cấp 13+ mẫu Agent dựng sẵn (Khối Doanh nghiệp: *Phòng Marketing, Phòng Kế toán, Phòng Nhân sự - HR, Phòng Kỹ thuật - IT, Phòng Kinh doanh - Sales*; mở rộng Giáo dục & Y tế) và cho phép Admin tự nhập bất kỳ tên Phòng ban / Chi nhánh / Dự án mới (`__CUSTOM__`).
* **`FR-05` (Client-side PDF Extraction & 3072-dim Vector RAG) [`✅`]:** Trích xuất trực tiếp nội dung file `.pdf` nhiều trang ngay trên trình duyệt bằng **Mozilla PDF.js**, chuẩn hóa UTF-8, phân mảnh theo đoạn văn (`\n\n`, lọc bỏ đoạn nhiễu $\le 25$ ký tự, giới hạn $2.000$ ký tự/chunk) và nhúng thành Vector **3.072 chiều** qua `models/gemini-embedding-001` lưu kèm nhãn `(tenant_id, department_access)`.
* **`FR-06` (Visual Workflow 3–5 Node Builder & Agent Versioning) [`🛠`]:** Giao diện Studio tích hợp khung thiết kế đồ thị luồng thực thi **3–5 Node chuẩn LangGraph** (`Input Guard Node` → `Disentangle & Intent Router Node` → `Pre-filtered RAG / Tool Node` → `HITL Approval Gate Node` → `Citation & Response Node`). Khi Admin bấm **`[Xuất bản (Publish)]`**, hệ thống đóng băng cấu hình thành phiên bản bất biến (`v1.0`, `v1.1`).
* **`FR-07` (MCP-like Tool Registry & Permission Manifest) [`✅` Core / `🛠` Mở rộng]:** Chuẩn hóa tối thiểu 3 công cụ nghiệp vụ:
  1. `leave_balance` (`read-only`): Tra cứu số ngày phép / hạn mức định mức còn lại của nhân viên.
  2. `leave_request_create` (`sensitive-write`): Khởi tạo đơn xin nghỉ phép / đề xuất ngân sách / yêu cầu cấp phát trình quản lý.
  3. `send_email` (`sensitive-write`): Gửi email thông báo xác nhận qua SMTP sau khi đề xuất được duyệt.
  Mỗi Tool được gắn **Permission Manifest** quy định rõ quyền tự động chạy (`auto_execute`) hay bắt buộc kích hoạt trạm dừng phê duyệt (`require_hitl = true`).

### 4.3. Phân hệ AI Context Core (Group Chat & RAG) & Phê duyệt HITL (`FR-08` → `FR-12`)
* **`FR-08` (Unit ACL Runtime Guardrail) [`✅`]:** Kiểm tra xác thực người dùng và đối chiếu cứng `user.department == agent.department_access` (hoặc `ALL`) ngay tại cổng API `/api/chat` trước khi gọi LLM. Nếu vi phạm, lập tức trả về thông báo từ chối truy cập (`ACL_DENIED`) và không tiêu tốn token LLM.
* **`FR-09` (Thread Disentanglement trong Group Chat) [`🛠`]:** Trong chế độ hội thoại nhóm đa thành viên, hệ thống phân tách các tin nhắn đan xen thành các luồng chủ đề độc lập (`thread_id`) bằng thuật toán lai 3 bước:
  1. Neo cấu trúc (`reply_to_msg_id`, `@mention`, khoảng cách thời gian $\Delta t \le 5\text{ phút}$).
  2. Gom cụm ngữ nghĩa bằng điểm tương đồng Cosine giữa vector 3.072 chiều của tin nhắn mới và trọng tâm (Centroid) các luồng đang mở.
  3. Gọi LLM phân xử nhẹ đối với các tin nhắn nằm ở vùng biên ($0.45 \le \text{sim} \le 0.65$).
* **`FR-10` (Temporal State Tracking — Quản lý Quyết định Bị Ghi đè) [`🛠`]:** Trích xuất các quyết định/lịch hẹn/phân công trong hội thoại và gắn trạng thái vòng đời (`ACTIVE`, `OVERRIDDEN`, `CANCELLED`, `DONE`). Khi một tin nhắn mới thay đổi hoặc hủy bỏ quyết định trước đó cùng chủ đề (`topic_key`), bản ghi cũ tự động chuyển sang `OVERRIDDEN` kèm con trỏ `superseded_by = msg_id_mới`. Khi người dùng yêu cầu tổng hợp hoặc hỏi đáp, Agent **chỉ sử dụng các quyết định có trạng thái `ACTIVE`**.
* **`FR-11` (Pre-filtered Vector Search & 2-Way Citation Grounding) [`✅` Doc Citation / `🛠` `#msg_id` Citation]:**
  - Tiền lọc cứng kho vector theo `tenant_id` (Lớp 1) và `department_access` (Lớp 2) trong `backend/vector_store.py`, chấm điểm **Cosine Similarity** (ngưỡng $> 0.35$) và sinh câu trả lời bằng `gemini-flash-latest` (`temperature = 0.2`).
  - Mọi câu trả lời bắt buộc đính kèm **Hộp Nguồn Trích dẫn (Citation Box)**: dẫn chiếu tên file tài liệu + điểm Cosine (đối với RAG) và/hoặc mã tin nhắn gốc `#msg_id` + người gửi (đối với thảo luận nhóm). Nếu không có dữ liệu vượt ngưỡng `0.35`, Agent trả lời rõ *"Không tìm thấy thông tin trong quy chế đơn vị"* thay vì tự suy diễn.
* **`FR-12` (Human-in-the-Loop Approval Workflow & Real-time Toast) [`✅`]:** Khi phát hiện ý định trình ký/đề xuất (`CREATE_REQUEST` hoặc gọi Tool `sensitive-write`), hệ thống tạm dừng (`interrupt_hitl = True`) để người dùng bấm xác nhận trên khung chat, lưu bản ghi `PENDING` vào CSDL, tăng bộ đếm chuông thông báo của `TENANT_ADMIN` và đẩy thông báo Toast thời gian thực về màn hình nhân viên ngay khi đề xuất được `APPROVED` hoặc `REJECTED`.

### 4.4. Kiến trúc Dữ liệu & Danh mục RESTful API (`FR-13` → `FR-14`)
* **`FR-13` (Cấu trúc CSDL Quan hệ Đồng bộ Kép `SQLite 3` & `MySQL 8.0`):
  - **5 Bảng cốt lõi đã vận hành (`✅`):**
    1. **`tenants`**: `id (PK)`, `name`, `contact_email`, `plan_type`, `domain_type` (`ENTERPRISE`/`EDUCATION`/`HEALTHCARE`/`CUSTOM`), `ui_schema` (JSON), `max_agents`, `max_employees`, `is_active`, `created_at`.
    2. **`users`**: `id (PK)`, `tenant_id (FK)`, `email`, `hashed_password`, `full_name`, `department` *(Đơn vị/Phòng ban)*, `role` (`SUPER_ADMIN`/`TENANT_ADMIN`/`EMPLOYEE`), `tenure_months`, `total_leave_days`, `used_leave_days`, `attributes` (JSON), `is_active`, `created_at`.
    3. **`agents`**: `id (PK)`, `tenant_id (FK)`, `name`, `description`, `instruction` *(System Prompt)*, `department_access` *(Phạm vi ACL)*, `is_published`, `creator_id`, `created_at` *(kèm cấu hình `workflow_json`, `tools_manifest`, `version` trong `🛠` MVP)*.
    4. **`documents`**: `id (PK)`, `tenant_id (FK)`, `file_name`, `file_path`, `file_size_kb`, `uploaded_at`.
    5. **`leave_requests` (HITL Operational Requests)**: `id (PK)`, `tenant_id (FK)`, `user_id`, `user_name`, `days_requested` *(Số lượng/Định mức)*, `date_details` *(Nội dung đề xuất)*, `status` (`PENDING` / `APPROVED` / `REJECTED`), `notified_to_user`, `created_at`.
  - **2 Bảng mở rộng cho Group Chat Context Core (`🛠` MVP):**
    6. **`chat_messages`**: `msg_id (PK)`, `tenant_id (FK)`, `department`, `sender_id`, `sender_name`, `reply_to_msg_id`, `thread_id`, `content`, `embedding_ref`, `created_at`.
    7. **`decision_states`**: `decision_id (PK)`, `tenant_id (FK)`, `thread_id`, `topic_key`, `summary_text`, `state` (`ACTIVE` / `OVERRIDDEN` / `CANCELLED` / `DONE`), `source_msg_id`, `superseded_by_msg_id`, `updated_at`.
* **`FR-14` (Danh mục RESTful API chính trong `backend/server.py`) [`✅`]:**
  - `GET / POST /api/tenants`, `GET / POST /api/tenants/ui_schema`, `POST /api/tenants/generate_schema`, `POST /api/tenants/delete`: Quản lý Công ty/Tổ chức & Động cơ UI Schema đa ngành.
  - `GET / POST /api/users`, `GET /api/users/<id_or_email>`, `POST /api/users/bulk`, `POST /api/users/update`, `POST /api/users/delete`: Quản lý Thành viên & Phòng ban + Đồng bộ Keycloak & Gmail SMTP.
  - `GET / POST /api/agents`: Khởi tạo, cấu hình & xuất bản Agent theo `tenant_id` và `department_access`.
  - `GET / POST /api/documents`: Tải lên tài liệu & kích hoạt nhúng Vector 3.072 chiều.
  - `POST /api/chat`: Cổng điều phối `LangGraphAgent` (Kiểm tra Identity & Unit ACL → Phân loại Intent / Tách luồng & Cập nhật trạng thái → Truy xuất Pre-filtered Vector RAG / Kích hoạt HITL → Trả về câu trả lời kèm Citation & X-Ray Trace).
  - `GET / POST /api/leave_requests`, `POST /api/leave_requests/decision`, `GET /api/notifications`: Luồng trình ký & thông báo duyệt HITL hai chiều thời gian thực.

---

## 5. Yêu cầu Phi chức năng (Non-Functional Requirements — NFRs)

* **`NFR-01` — Hiệu năng & Độ trễ (Latency & Throughput):**
  - Thời gian phản hồi cho truy vấn RAG hoặc gọi Tool đơn lượt: **P50 $\le 1.5\text{ giây}$, P95 $< 3.0\text{ giây}$**.
  - Thời gian xử lý tách luồng và tổng hợp trạng thái hội thoại nhóm phức tạp (15–30 tin nhắn đan xen): **P95 $< 8.0\text{ giây}$**.
  - Thời gian chặn truy cập trái phép tại cổng Unit ACL (`ACL_DENIED`): **$< 0.05\text{ giây}$** (chặn trước khi gọi API LLM).
* **`NFR-02` — Bảo mật & Cô lập Dữ liệu Đa tầng (Zero Data Leakage):**
  - **0% rò rỉ dữ liệu** giữa các công ty (`tenant_id`) hoặc giữa các phòng ban không được cấp quyền (`department_access`) nhờ cơ chế kiểm tra kép ở cả tầng API và tầng Pre-retrieval Vector Store.
  - Mật khẩu người dùng được quản lý xác thực qua **Keycloak OIDC SSO** (PBKDF2/Argon2) và truyền tải qua phiên làm việc có kiểm soát.
* **`NFR-03` — Độ tin cậy, Đồng bộ CSDL Kép & Khả năng Thích ứng (Reliability & Portability):**
  - Mọi thao tác ghi (`INSERT / UPDATE / DELETE`) trên SQLite nội bộ đều được lớp `AutoSyncSQLiteConnection` (`backend/mysql_sync.py`) nhân bản tự động theo thời gian thực sang **MySQL 8.0 Server** (`mini_agent_studio`). Nếu máy chủ MySQL hoặc Keycloak tạm ngắt, ứng dụng có cơ chế fallback an toàn để không làm gián đoạn quá trình demo.
* **`NFR-04` — Khả năng Mở rộng Đa Ngành (Domain Extensibility):**
  - Thêm một công ty thuộc ngành nghề hoàn toàn mới (Logistics, Ngân hàng, Bán lẻ, Luật, Giáo dục, Y tế...) chỉ thông qua cấu hình JSON của `schema_engine.py` trong **$< 30\text{ giây}$** mà không cần thay đổi cấu trúc bảng CSDL hay viết lại mã nguồn giao diện.

---

## 6. Tiêu chí Hoàn thành & Nghiệm thu (Acceptance Criteria — Definition of Done)

Hệ thống được đánh giá đạt chuẩn nghiệm thu khi vượt qua đầy đủ **7 kịch bản kiểm thử (Pass/Fail)** sau:

| Mã AC | Hạng mục Kiểm thử | Điều kiện Đạt (Pass Criteria) | Trạng thái |
| :--- | :--- | :--- | :---: |
| **`AC-01`** | **Cấp phát Công ty Đa ngành & SSO** | `SUPER_ADMIN` tạo một công ty mới (VD: Công ty Bán lẻ hoặc Tập đoàn Sản xuất), hệ thống tự sinh `ui_schema` tương ứng, tự động tạo tài khoản trên Keycloak SSO và gửi email mật khẩu thành công qua Gmail SMTP. | `✅ Đạt` |
| **`AC-02`** | **Khởi tạo Agent & Nạp PDF Vector 3072-dim** | `TENANT_ADMIN` tạo Agent mới cho một phòng ban (VD: *Phòng Marketing* hoặc phòng ban tự nhập mới), kéo thả file PDF quy chế nhiều trang; hệ thống bóc tách văn bản, nhúng vector 3.072 chiều và xuất bản Agent trong $< 3\text{ phút}$. | `✅ Đạt` |
| **`AC-03`** | **Cô lập Quyền Truy cập theo Phòng ban (Unit ACL)** | Nhân viên thuộc *Phòng Marketing* chat bình thường với *Agent Phòng Marketing* và *Agent Toàn công ty (`ALL`)*, nhưng khi cố tình gọi *Agent Phòng Kế toán* hoặc hỏi dữ liệu Kế toán sẽ bị chặn cứng (`ACL_DENIED`) với 0% dữ liệu bị lộ. | `✅ Đạt` |
| **`AC-04`** | **Trích dẫn Nguồn Chính xác & Chống Ảo giác** | Khi hỏi nội dung có trong quy chế PDF, Agent trả lời đúng kèm **Hộp Nguồn Trích dẫn** (tên file + điểm Cosine $> 0.35$). Khi hỏi thông tin ngoài tài liệu, Agent từ chối suy diễn. | `✅ Đạt` |
| **`AC-05`** | **Chốt chặn Phê duyệt Con người (HITL End-to-End)** | Khi nhân viên yêu cầu *"Tạo đề xuất duyệt ngân sách"* hoặc *"Xin nghỉ phép"*, Agent dừng lại hiện nút xác nhận HITL $\rightarrow$ Lưu trạng thái `PENDING` trên SQLite & MySQL Workbench $\rightarrow$ Admin bấm `[Duyệt]` $\rightarrow$ Màn hình nhân viên nổ thông báo Toast thời gian thực. | `✅ Đạt` |
| **`AC-06`** | **Tách Luồng Hội thoại Nhóm (Thread Disentanglement)** | Trong khung Group Chat Sandbox có $\ge 3$ luồng chủ đề đan xen (VD: bàn ngân sách, đổi lịch họp, hỏi quy trình), Agent phân tách đúng các tin nhắn về từng `thread_id` (Micro-F1 $\ge 0.72$) và không ghép nhầm thông tin giữa các luồng. | `🛠 MVP` |
| **`AC-07`** | **Theo dõi Quyết định Bị Ghi đè (Temporal State)** | Khi lịch họp hoặc quyết định trong nhóm bị thay đổi từ phương án A sang phương án B rồi chốt phương án B, Agent đánh dấu A là `OVERRIDDEN`, B là `ACTIVE`, và khi được hỏi chỉ trả lời phương án B kèm trích dẫn `#msg_id`. | `🛠 MVP` |

---

## 7. Chỉ số Thành công, Bộ Dữ liệu Benchmark & Bảng Đối chiếu Thực tế Triển khai

### 7.1. Bộ Chỉ số Thành công Định lượng (KPIs) & Benchmark Nghiệm thu
Các chỉ số dưới đây được đồng bộ 100% với **Mục 5 của `Brief.md`**:
- **Bảo mật & Cô lập đơn vị (Unit ACL & Tenant Isolation):** **100%** (0% rò rỉ dữ liệu trên $\ge 50$ kịch bản Red-team vượt quyền giữa các phòng ban và các công ty).
- **Tuân thủ Phê duyệt Con người (HITL Interception Rate):** **100%** các tác vụ nhạy cảm (`sensitive-write`) được chặn để chờ phê duyệt.
- **Độ chính xác Tách luồng Hội thoại (Thread Disentanglement Micro-F1):** **$\ge 0.72$** (mức cơ sở MVP) $\rightarrow$ **$\ge 0.85$** (mục tiêu nâng cao), kiểm chứng trên **Ubuntu Chat Disentanglement Dataset** và tập hội thoại nhóm nội bộ.
- **Độ chính xác Trạng thái Thời gian (Temporal State Tracking):** Accuracy **$\ge 80\%$**, tỷ lệ sử dụng lại quyết định cũ đã hủy (Stale-decision Usage Rate) **$\le 5\%$**.
- **Độ trung thực & Độ phủ Trích dẫn (Citation Grounding):** Faithfulness **$\ge 90\%$**, Coverage **$\ge 95\%$**, kiểm chứng theo chuẩn **SAMSum / DialogSum / MeetingBank**.
- **Hiệu năng Phản hồi (End-to-End Latency):** **P50 $\le 1.5\text{s}$, P95 $< 3.0\text{s}$** cho truy vấn đơn lượt; **P95 $< 8.0\text{s}$** cho tác vụ tách luồng & tổng hợp hội thoại nhóm; kiểm chứng khả năng gọi công cụ theo chuẩn **MultiWOZ / $\tau$-bench**.

---

### 7.2. Bảng Đối chiếu Minh bạch: Bản Dựng Hiện tại vs. Mục tiêu Hoàn thiện MVP vs. Lộ trình Phase 2

| Hạng mục Kỹ thuật | `✅` Đã chạy hoàn chỉnh trong Bản dựng Hiện tại (Current Prototype) | `🛠` Cam kết Hoàn thiện trong Phạm vi MVP (CHAT-40 Target) | `🚀` Lộ trình Nâng cấp Phase 2 (Production Scaling) |
| :--- | :--- | :--- | :--- |
| **1. Định vị Đa Ngành & Quản trị Tổ chức** | **Adaptive UI Schema Engine** (`backend/schema_engine.py`) hỗ trợ mọi công ty (`ENTERPRISE` trọng tâm + `EDUCATION`, `HEALTHCARE`, `CUSTOM`), quản lý nhân sự/đơn vị & nhập CSV. | Bổ sung bộ mẫu Prompt & biểu mẫu HITL chuyên sâu cho các ngành Tài chính, Bán lẻ, Sản xuất, Logistics. | Cổng tự phục vụ (Self-service Onboarding) & Quản lý hạn mức Quota/Billing tự động. |
| **2. Xác thực & Cấp phát Định danh** | **Keycloak OIDC SSO** (`localhost:8080`, Realm `mini-agent-platform`) + gửi mật khẩu tự động qua **Google Gmail SMTP** (`backend/mailer.py`). | Xác thực chữ ký JWT trực tiếp tại tầng Middleware cho mọi API nội bộ và băm `bcrypt` cho mật khẩu dự phòng. | Tích hợp SAML 2.0 / Azure AD (Entra ID) & Google Workspace SSO cho tập đoàn lớn. |
| **3. No-Code Studio & Workflow** | Tạo Agent 1-Click (13+ mẫu) hoặc tự nhập đơn vị mới (`__CUSTOM__`), cấu hình System Prompt, ACL và kiểm thử Live Playground. | Trình kéo thả **Workflow 3–5 Node (React Flow)**, cấu hình **Permission Manifest** cho $\ge 3$ Tools và đóng băng phiên bản **Agent Versioning (`v1.0`, `v1.1`)**. | Node rẽ nhánh điều kiện động (`Conditional Branching`), AI tự sinh Workflow từ câu lệnh tự nhiên & 1-click Rollback. |
| **4. Kho Tri thức Vector RAG & ACL** | Bóc tách PDF qua `Mozilla PDF.js`, chia đoạn văn `\n\n`, nhúng Vector **3.072 chiều** (`gemini-embedding-001`) kèm **Pre-filtering ACL** 2 lớp (`tenant_id` + `department_access`). | Chuẩn hóa **Recursive Character Text Splitter** (`chunk_size = 500`, `overlap = 100`) và gắn metadata chương/điều khoản chi tiết. | Chuyển đổi sang cụm máy chủ Vector phân tán **Qdrant / Milvus** kết hợp Hybrid Search (BM25 + Dense Vector). |
| **5. AI Context Core & Group Chat** | Điều phối `LangGraphAgent` 2 Node (Intent Routing + Pre-filtered RAG & HITL Interrupt) kèm **Document Citation Box**. | **Group Chat Sandbox (Role Switcher)** + **Thread Disentanglement** + **Temporal State Tracking (`ACTIVE`/`OVERRIDDEN`)** + **Trích dẫn mã tin nhắn (`#msg_id`)**. | Kết nối trực tiếp Webhook thời gian thực với Slack, Microsoft Teams, Zalo OA và Discord. |
| **6. Hạ tầng CSDL & Giám sát (Observability)** | CSDL kép **SQLite 3** đồng bộ tức thì sang **MySQL 8.0 Workbench** (`backend/mysql_sync.py`); hiển thị **X-Ray Telemetry Trace** (`intent`, `latency`, `tokens`, `cosine`) trên UI. | Tích hợp trực tiếp **Langfuse Python SDK** và bộ script chạy kiểm thử định lượng tự động (`eval_runner.py`). | Chuyển đổi Backend sang `FastAPI` + `PostgreSQL` bất đồng bộ và thiết lập CI/CD Regression Gate tự động. |
