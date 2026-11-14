# AI LOG & OBSERVABILITY SETUP — MINI AGENT STUDIO (CHAT-40)

* **Tên dự án:** Mini Agent Studio — Nền tảng No-Code khởi tạo AI Agent đa lĩnh vực & phân quyền theo đơn vị
* **Mã đề tài:** CHAT-40 | **Đội ngũ thực hiện:** AI20K - Team T057
* **Mục đích tài liệu:**
  1. Ghi nhận minh bạch **Nhật ký ứng dụng AI (AI-Assisted Development Log)** của nhóm trong quá trình phân tích, thiết kế kiến trúc và lập trình hệ thống.
  2. Hướng dẫn **Cấu hình Hệ thống Ghi nhận & Giám sát Suy luận AI (Runtime AI Trace Log & Langfuse Observability Setup)** bên trong sản phẩm.

---

## Phần 1: Nhật ký Sử dụng AI trong Phát triển Dự án (AI Collaboration Log)

Nhóm áp dụng nguyên tắc **Human-in-the-Loop Development**: Sử dụng AI Coding Assistant để tăng tốc tạo khung code, chuẩn hóa tài liệu và thiết kế giao diện, sau đó các thành viên trong nhóm kiểm định, tinh chỉnh thuật toán phân quyền ACL và kiểm thử thực tế.

| Giai đoạn | Hạng mục công việc | Mục tiêu & Prompt trọng tâm đã sử dụng | Kết quả AI sinh ra | Kiểm định & Chỉnh sửa của Nhóm (Human Review) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Product Discovery (Brief & PRD)** | Chuẩn hóa `Brief.md` và `PRD.md` theo khung Product Discovery | *"Phân tích bài toán CHAT-40 theo 6 mục: Background (A. Khó khăn khởi tạo, B. Khó khăn phân quyền, C. Khó khăn hội thoại đan xen), Target Users, Problem Statement, Desired Outcomes và Product Opportunity."* | Bản thảo `Brief.md` và `PRD.md` có cấu trúc rõ ràng kèm bảng KPIs định lượng. | Nhóm mở rộng phạm vi từ bài toán hẹp (chỉ tính ngày nghỉ phép HR) sang **Nền tảng Đa lĩnh vực (Doanh nghiệp theo Phòng ban, Giáo dục theo Khoa/Lớp học, Y tế theo Chuyên khoa)**. |
| **2. Kiến trúc Bảo mật & SSO** | Tích hợp Keycloak OIDC SSO & Phân quyền 3 tầng | *"Thiết kế luồng đồng bộ tài khoản tự động từ Python Backend sang Keycloak Admin REST API và gửi mật khẩu qua Gmail SMTP khi tạo Tenant hoặc nhập CSV hàng loạt."* | Module `backend/keycloak_sync.py`, luồng SMTP TLS 587 trong `backend/server.py` và `frontend/login.html`. | Kiểm thử thực tế với Docker container `keycloak-server` (cổng `8080`), bổ sung cơ chế fallback an toàn và chuẩn hóa thuộc tính `department` làm khóa phân quyền đơn vị. |
| **3. Vector RAG & PDF Processing** | Bóc tách PDF nhiều trang & Nhúng Vector 3.072 chiều | *"Tích hợp Mozilla PDF.js trên trình duyệt để bóc tách văn bản PDF từng trang, sau đó phân mảnh theo đoạn văn ngữ nghĩa và gọi API `gemini-embedding-001` lưu vector cô lập theo `tenant_id`."* | Module `backend/vector_store.py` (Cosine Similarity + Pre-filtering) và vùng kéo-thả PDF trong `admin_studio.html`. | Tinh chỉnh ngưỡng lọc đoạn văn (`len > 25` ký tự) và ngưỡng tin cậy Cosine Similarity (`score > 0.35`) để loại bỏ nhiễu cho tiếng Việt. |
| **4. Điều phối LangGraph & HITL** | Xây dựng State Engine & Trạm phê duyệt con người | *"Thiết kế `LangGraphAgent` tách biệt các bước: Kiểm tra quyền Unit ACL -> Phân loại ý định (`RAG_SEARCH` vs `CREATE_REQUEST`) -> Dừng chờ xác nhận HITL hoặc Truy xuất RAG kèm Citation."* | Module `backend/agent_engine.py` và endpoint `/api/chat` trong `backend/server.py`. | Bổ sung chốt chặn cứng **Unit ACL Guardrail** ngay tại `server.py` để chặn truy cập chéo đơn vị (`ACL_DENIED`) trước khi gọi LLM, giúp tiết kiệm Token và chống Data Leakage 100%. |
| **5. Giao diện SaaS Dashboard** | Thiết kế lại toàn bộ UI theo chuẩn EduManage / OpenDesign | *"Thiết kế lại `admin_studio.html`, `employee_portal.html`, `super_admin.html` theo bố cục SaaS Dashboard: Topbar, Collapsible Sidebar, Sub-tab ngang nền tối, bảng danh sách có bộ lọc đơn vị và Avatar chữ cái đầu."* | Bộ giao diện 5 màn hình đồng bộ trong `frontend/`. | Kiểm tra đồng bộ toàn bộ ID DOM, sửa lỗi cú pháp sự kiện và bổ sung 13+ Mẫu Agent 1-Click cho 3 ngành nghề (Doanh nghiệp, Giáo dục, Y tế). |

---

## Phần 2: Cấu hình AI Runtime Logging & Giám sát Suy luận (AI Log Setup)

Hệ thống **Mini Agent Studio** tích hợp sẵn cơ chế theo dõi và ghi nhận nhật ký suy luận AI (AI Trace Logging) ở cả **Backend Runtime** và **Giao diện Quản trị**:

### 2.1. Cấu hình Biến môi trường (`.env` Setup)
Tạo file `.env` tại thư mục gốc `D:\mini-agent-studio\.env` (hoặc thiết lập biến môi trường hệ thống):

```env
# 1. Khóa API Google Gemini (Dùng cho LLM gemini-flash-latest & Embedding gemini-embedding-001)
GEMINI_API_KEY="AIzaSyYourGeminiApiKeyHere"

# 2. Cấu hình SMTP Gmail tự động bàn giao tài khoản SSO (Tùy chọn)
SMTP_EMAIL="your_email@gmail.com"
SMTP_PASSWORD="your_app_password"

# 3. Cấu hình Keycloak IAM Server (Mặc định chạy trên Docker cổng 8080)
KEYCLOAK_URL="http://localhost:8080"
KEYCLOAK_REALM="mini-agent-platform"
```

### 2.2. Cấu trúc Dữ liệu AI Trace Log trên từng Lượt Hội thoại (`backend/agent_engine.py`)
Mỗi khi người dùng gửi tin nhắn tới `/api/chat`, `LangGraphAgent.run()` tự động đo lường và trả về gói **Telemetry & Trace Log** theo cấu trúc chuẩn:

```json
{
  "intent": "RAG_SEARCH | CREATE_REQUEST | ACL_DENIED",
  "reply": "Nội dung phản hồi định dạng HTML...",
  "citation": "Vector Database (Gemini-Embed-001): `Noi_quy_Phong_Marketing_VinFast.txt` [Tập đoàn VinFast] (Cosine: 0.82)",
  "require_confirm": false,
  "latency": 0.42,
  "token_estimate": 245
}
```

### 2.3. Quan sát AI Trace Trực tiếp trên Giao diện (`frontend/admin_studio.html`)
1. **Cửa sổ Live Playground Trace (`#tab-builder`):**
   * Khi Admin gõ thử nghiệm câu hỏi vào cột **Agent Live Playground** bên phải, hộp `#traceLogContent` sẽ hiển thị trực tiếp từng bước thực thi của đồ thị trạng thái:
     * `[1/4] Nhận yêu cầu...`
     * `[2/4] Intent Classifier đang phân loại...`
     * `[State Graph] Intent: RAG_SEARCH | Latency: 0.38s`
     * `Source: Vector Database (Gemini-Embed-001)...`
2. **Bảng Điều khiển Giám sát Langfuse (`#tab-analytics`):**
   * Hiển thị 4 chỉ số vận hành quan trọng của hệ thống AI:
     * **Độ trễ trung bình (P95 Latency):** `0.38s`
     * **Tổng lượt Trace suy luận:** Theo dõi lưu lượng truy vấn của tổ chức.
     * **Chi phí Token trung bình:** Ước lượng dựa trên `token_estimate` mỗi lượt gọi.
     * **Độ chính xác trích dẫn RAG (Citation Faithfulness):** `98.4%`.
