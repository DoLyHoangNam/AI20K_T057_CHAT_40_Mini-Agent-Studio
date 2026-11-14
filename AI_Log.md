# AI LOG & OBSERVABILITY SETUP — MINI AGENT STUDIO (CHAT-40)

* **Tên dự án:** Mini Agent Studio — Nền tảng No-Code khởi tạo AI Agent đa lĩnh vực & phân quyền theo đơn vị
* **Mã đề tài:** CHAT-40 | **Đội ngũ thực hiện:** AI20K - Team T057
* **Mục đích tài liệu:**
  1. Ghi nhận minh bạch **Nhật ký ứng dụng AI (AI-Assisted Development Log)** của nhóm trong quá trình phân tích, thiết kế kiến trúc, lập trình và rà soát lỗi bảo mật.
  2. Hướng dẫn **Cấu hình Hệ thống Biến môi trường (`backend/.env`) & Giám sát Suy luận AI (Runtime AI Trace Log)** bên trong sản phẩm.

---

## Phần 1: Nhật ký Sử dụng AI trong Phát triển Dự án (AI Collaboration Log)

Nhóm áp dụng nguyên tắc **Human-in-the-Loop Engineering**: Sử dụng AI Assistant để tăng tốc tạo khung code, chuẩn hóa tài liệu và thiết kế giao diện, sau đó các thành viên trực tiếp kiểm định chéo với CSDL, phát hiện lỗ hổng logic và tinh chỉnh lại thuật toán phân quyền ACL.

| Giai đoạn | Hạng mục công việc | Mục tiêu & Prompt trọng tâm đã sử dụng | Kết quả AI sinh ra | Kiểm định & Chỉnh sửa Thực tế của Nhóm (Human Review & Fixes) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Product Discovery (`Brief.md` & `PRD.md`)** | Chuẩn hóa hồ sơ đề tài theo khung Product Discovery | *"Phân tích bài toán CHAT-40 theo 6 mục: Background (Khó khăn khởi tạo, Phân quyền dữ liệu, Hội thoại đan xen), Target Users, Problem Statement, Desired Outcomes và Architecture."* | Bản thảo `Brief.md` và `PRD.md` có cấu trúc rõ ràng kèm bảng KPIs định lượng. | Nhóm mở rộng phạm vi sang **Nền tảng Đa lĩnh vực (`backend/schema_engine.py`)** gồm Doanh nghiệp (Phòng ban), Giáo dục (Khoa/Lớp học), Y tế (Chuyên khoa) và bổ sung **Mục 7 trong `PRD.md`** phân định rõ tính năng *MVP Demo 1* và *Phase 2 Roadmap*. |
| **2. Định danh SSO & Đồng bộ Tài khoản** | Tích hợp Keycloak OIDC SSO & Gmail SMTP | *"Thiết kế luồng đồng bộ tài khoản tự động từ `backend/server.py` sang Keycloak Admin REST API (`localhost:8080`) và gửi mật khẩu qua Gmail SMTP (`backend/mailer.py`) khi tạo Tenant hoặc nhập CSV."* | Hàm `sync_user_to_keycloak()` trong `backend/server.py`, module `backend/mailer.py` và trang `frontend/login.html`. | **Phát hiện & sửa lỗi lệch ID:** Token Keycloak trả về `sub` dạng UUID trong khi SQLite dùng `id` số nguyên. Nhóm đã nâng cấp `/api/users/<id_or_email>` và `login.html` để tự động ánh xạ qua `email` ngay sau khi xác thực OIDC. |
| **3. Vector RAG & Pre-retrieval ACL** | Bóc tách PDF nhiều trang & Nhúng Vector 3.072 chiều | *"Tích hợp Mozilla PDF.js trên trình duyệt để bóc tách văn bản PDF từng trang, sau đó chia đoạn văn `\n\n` và gọi API `models/gemini-embedding-001` lưu vào `backend/vector_index.json`."* | Module `backend/vector_store.py` (Cosine Similarity) và vùng kéo-thả PDF trong `frontend/admin_studio.html`. | **Phát hiện & vá lỗ hổng Data Leakage:** Bản đầu tiên chỉ lọc Vector theo `tenant_id`. Nhóm đã bổ sung **Lớp lọc thứ 2 (`_infer_chunk_department`)** ngay trong `vector_search()` để chặn nhân viên phòng khác dùng Agent chung (`ALL`) truy xuất lén tài liệu của phòng Marketing/Kế toán. |
| **4. Điều phối `LangGraphAgent` & HITL** | Xây dựng State Engine 2 Node & Trạm phê duyệt con người | *"Thiết kế `LangGraphAgent` trong `backend/agent_engine.py`: Node 1 phân loại ý định (`CREATE_REQUEST` vs `RAG_SEARCH`) và kích hoạt HITL Interrupt; Node 2 truy xuất Vector RAG và gọi `gemini-flash-latest` kèm Citation."* | Module `backend/agent_engine.py` và endpoint `/api/chat` trong `backend/server.py`. | **Loại bỏ Fallback nguy hiểm:** Sửa `/api/chat` không tự động gán user mặc định sang `VINFAST` khi không tìm thấy user, đồng thời nạp `backend/.env` trước khi import `agent_engine.py` để đảm bảo `GEMINI_API_KEY` luôn sẵn sàng. |
| **5. Giao diện SaaS Dashboard** | Thiết kế UI theo chuẩn EduManage / Clean SaaS | *"Thiết kế `admin_studio.html`, `employee_portal.html`, `super_admin.html` theo bố cục SaaS Dashboard: Topbar, Collapsible Sidebar, Sub-tab ngang nền tối, bảng danh sách có bộ lọc đơn vị và 13 Mẫu Agent 1-Click."* | Bộ giao diện 5 màn hình đồng bộ trong `frontend/` (`login`, `super_admin`, `admin_studio`, `employee_portal`, `database_viewer`). | Làm sạch dữ liệu mồi (`backend/database.db`) cho 4 tổ chức (`PLATFORM`, `VINFAST`, `VNU`, `BVQT`) và kiểm tra toàn bộ luồng duyệt đơn HITL + thông báo Toast thời gian thực. |

---

## Phần 2: Cấu hình Biến môi trường & Giám sát Suy luận (AI Log Setup)

Hệ thống **Mini Agent Studio** tích hợp cơ chế nạp cấu hình bảo mật từ `backend/.env` và ghi nhận nhật ký suy luận AI (Runtime Trace Logging) trực tiếp trên từng lượt hội thoại:

### 2.1. Cấu hình Biến môi trường (`backend/.env`)
Tạo file `backend/.env` (đã được đưa vào `.gitignore` để bảo mật tuyệt đối khóa API, xem mẫu tại `backend/.env.example`):

```env
# 1. Khóa API Google Gemini (Dùng cho LLM gemini-flash-latest & Embedding gemini-embedding-001)
GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere

# 2. Cấu hình Gmail SMTP tự động gửi mật khẩu khi tạo Tenant / Thành viên mới
SMTP_USER=your_gmail@gmail.com
SMTP_PASS=your_google_app_password

# 3. Mật khẩu Quản trị Keycloak IAM Server (Mặc định chạy trên cổng 8080)
KC_ADMIN_PASS=admin123
```

> **Lưu ý kỹ thuật:** Hàm `_load_backend_env()` tại đầu file `backend/server.py` tự động nạp `backend/.env` vào `os.environ` trước khi khởi tạo `agent_engine.py` và `vector_store.py`.

### 2.2. Cấu trúc Dữ liệu AI Trace Log trên từng Lượt Hội thoại (`backend/agent_engine.py`)
Mỗi khi người dùng gửi tin nhắn tới `POST /api/chat`, phương thức `LangGraphAgent.run()` tự động đo thời gian xử lý thực tế (`latency`), ước lượng số lượng token (`token_estimate`) và trả về gói **Telemetry & Trace Log**:

```json
{
  "intent": "RAG_SEARCH | CREATE_REQUEST | ACL_DENIED | AUTH_REQUIRED",
  "reply": "Nội dung phản hồi định dạng HTML...",
  "citation": "Vector Database (Gemini-Embed-001): `Noi_quy_Phong_Marketing_VinFast.txt` [Tập đoàn VinFast] (Cosine: 0.87)",
  "require_confirm": false,
  "latency": 0.42,
  "token_estimate": 245
}
```

### 2.3. Quan sát AI Trace Trực tiếp trên Giao diện (`frontend/admin_studio.html`)
1. **Cửa sổ Live Playground Trace (`#tab-builder`):**
   * Khi Admin gõ thử nghiệm câu hỏi vào cột **Agent Live Playground** bên phải, hộp `#traceLogContent` hiển thị trực tiếp từng bước thực thi từ phản hồi thực của `/api/chat`:
     * `[1/4] Nhận yêu cầu...`
     * `[2/4] Intent Classifier đang phân loại...`
     * `[State Graph] Intent: RAG_SEARCH | Latency: 0.42s`
     * `Source: Vector Database (Gemini-Embed-001)...`
2. **Bảng Điều khiển Giám sát (`#tab-analytics`):**
   * Giao diện mô phỏng bảng chỉ số vận hành AI (Độ trễ P95, Lưu lượng truy vấn, Ước lượng Token và Độ trung thực trích dẫn RAG), sẵn sàng để kết nối trực tiếp với `langfuse` SDK trong giai đoạn Phase 2.
