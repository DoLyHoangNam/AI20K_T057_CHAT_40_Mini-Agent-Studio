# PROJECT BRIEF: MINI AGENT STUDIO (CHAT-40)

**Tên dự án:** Nền tảng No-Code khởi tạo AI Agent cho mọi Công ty & Tổ chức, xử lý đan xen hội thoại nhóm & phân quyền cô lập theo đơn vị  
**Mã đề tài:** CHAT-40 | **Nhóm thực hiện:** AI20K - Team T057  
**Định vị sản phẩm:** Giải pháp SaaS Multi-Tenant phục vụ **mọi loại hình công ty và doanh nghiệp** (trọng tâm), đồng thời mở rộng linh hoạt sang Giáo dục, Y tế và bất kỳ tổ chức đa đơn vị nào nhờ **Adaptive UI Schema Engine**.  
**Trạng thái tài liệu:** Phiên bản hoàn chỉnh & Định lượng (Đồng bộ 100% với `PRD.md` & `Wireframe_UI_Flow.md`)

---

## 1. Bối cảnh & Tuyên bố Bài toán (Background & Problem Statement)

### 1.1. Bối cảnh Chuyển đổi số & Khả năng Ứng dụng Phổ quát cho Mọi Công ty
Trong kỷ nguyên AI tạo sinh, **bất kỳ công ty hay tổ chức nào** — từ Công nghệ, Tài chính - Ngân hàng, Sản xuất, Bán lẻ, Logistics cho đến Dịch vụ, Giáo dục hay Y tế — đều được cấu trúc thành các **Đơn vị chuyên môn (Operating Units / Departments)** với quy chế, tài liệu mật và quy trình phê duyệt riêng biệt.

Để một nền tảng AI Agent có thể phục vụ **tất cả các công ty** mà không phải đập đi xây lại mã nguồn cho từng ngành, **Mini Agent Studio (CHAT-40)** trừu tượng hóa mọi tổ chức về 4 thực thể lõi (`Tổ chức / Tenant` → `Đơn vị / Unit` → `Thành viên / Member` → `Trợ lý AI & Luồng duyệt HITL`):

| Thực thể Lõi Hệ thống (`Core Schema`) | Kịch bản Trọng tâm: Mọi Công ty & Doanh nghiệp (`ENTERPRISE` — Công nghệ, Ngân hàng, Sản xuất, Bán lẻ, Logistics...) | Ví dụ Mở rộng 1: Khối Giáo dục & Đào tạo (`EDUCATION`) | Ví dụ Mở rộng 2: Khối Y tế & Bệnh viện (`HEALTHCARE`) | Ví dụ Mở rộng 3: Tổ chức Bất kỳ Khác (`CUSTOM` — Luật, BĐS, NGO...) |
| :--- | :--- | :--- | :--- | :--- |
| **Tổ chức (`tenant_id`)** | Công ty / Tập đoàn (VD: VinFast, FPT, Vietcombank, Masan...) | Trường Đại học / Học viện (VD: ĐHQG, VinUni...) | Bệnh viện / Hệ thống phòng khám | Công ty Luật, Sàn BĐS, Tổ chức phi chính phủ |
| **Đơn vị (`department`)** | Phòng ban / Chi nhánh / Dự án (*Marketing, Kế toán, HR, IT, Sales, Pháp chế, Chuỗi cung ứng...*) | Khoa / Viện / Lớp học / Phòng chức năng (*Phòng Đào tạo, Khoa CNTT, Lớp AI-K68...*) | Chuyên khoa / Bộ phận (*Khoa Nội, Khoa Dược, Hành chính viện...*) | Ban chuyên môn / Nhóm dự án / Chi nhánh vùng |
| **Thành viên (`user.role`)** | Ban Giám đốc, Trưởng phòng (`TENANT_ADMIN`), Nhân viên (`EMPLOYEE`) | Giáo vụ khoa, Giảng viên chủ nhiệm (`TENANT_ADMIN`), Sinh viên (`EMPLOYEE`) | Trưởng khoa (`TENANT_ADMIN`), Bác sĩ / Điều dưỡng (`EMPLOYEE`) | Quản lý đơn vị (`TENANT_ADMIN`), Chuyên viên (`EMPLOYEE`) |
| **Kho tri thức (`Vector RAG`)** | Sổ tay nhân sự, định mức ngân sách, SOP vận hành, hợp đồng mẫu, tài liệu kỹ thuật | Quy chế đào tạo, đề cương môn học, lịch thi, hướng dẫn đồ án | Phác đồ điều trị, danh mục thuốc bảo hiểm, quy trình hội chẩn | Hồ sơ pháp lý, bảng hàng dự án, quy trình kiểm toán |
| **Tác vụ trình duyệt (`HITL`)** | Duyệt ngân sách chiến dịch, xin nghỉ phép, mua sắm thiết bị, xuất kho, duyệt hợp đồng | Xin hoãn thi, đăng ký học phần, mượn phòng lab, duyệt đề tài | Duyệt cấp phát thuốc đặc trị, đề xuất hội chẩn liên khoa | Phê duyệt hồ sơ tư vấn, giải ngân, cấp quyền truy cập |

> **Trọng tâm triển khai:** Tài liệu này lấy **Khối Doanh nghiệp / Công ty (`ENTERPRISE`)** làm kịch bản xuyên suốt để chứng minh chiều sâu kỹ thuật. Các lĩnh vực Giáo dục (`EDUCATION`), Y tế (`HEALTHCARE`) và Tùy chỉnh (`CUSTOM`) được tích hợp sẵn trong `backend/schema_engine.py` như những minh chứng thực tế cho khả năng thích ứng đa ngành của nền tảng.

---

### 1.2. Nỗi đau Cốt lõi tại các Công ty hiện nay (Core Pain Points)
Quá trình đưa AI Agent vào vận hành thực tế tại các công ty đang vấp phải **3 điểm nghẽn cụ thể**:

1. **Rào cản kỹ thuật khi khởi tạo Agent theo từng phòng ban (No-Code Barrier):**
   - *Tình huống cụ thể:* Trưởng phòng Nhân sự (HR), Trưởng phòng Kế toán hay Trưởng phòng Marketing là người nắm rõ nhất quy chế và biểu mẫu của phòng mình nhưng không biết lập trình Python/LangChain để tự viết System Prompt, cắt nhỏ (chunking) tài liệu PDF hay kết nối Tool. Ngược lại, nếu mọi yêu cầu tạo/sửa bot đều dồn về phòng IT thì mất từ 2–4 tuần cho mỗi phòng ban.
2. **Nguy cơ lộ lọt dữ liệu chéo giữa các phòng ban & thiếu chốt chặn phê duyệt (Security & HITL Gap):**
   - *Tình huống cụ thể:* Trong một công ty, dữ liệu bảng lương của Phòng HR, báo cáo tài chính của Phòng Kế toán hay chiến lược giá của Phòng Marketing là tối mật. Nếu dùng chung một Chatbot RAG toàn công ty không có cơ chế lọc cứng theo đơn vị (Unit ACL), nhân viên phòng Kinh doanh có thể hỏi khéo (Prompt Injection) để trích xuất chính sách thưởng nội bộ của phòng Kế toán. Đồng thời, khi nhân viên yêu cầu AI thực hiện tác vụ có tính cam kết (như *"Tạo đề xuất chi 50 triệu ngân sách TikTok"* hoặc *"Nộp đơn nghỉ phép 4 ngày"*), việc để AI tự động ghi nhận vào hệ thống mà không qua bước phê duyệt của Trưởng phòng (**Human-in-the-Loop**) gây rủi ro vận hành nghiêm trọng.
3. **Hỗn loạn ngữ cảnh trong Hội thoại Nhóm phòng ban (Group Chat Context Chaos):**
   - *Tình huống cụ thể:* Trong phòng chat chung của một phòng ban hoặc dự án, nhân viên trao đổi đan xen nhiều chủ đề cùng lúc (vừa hỏi định mức công tác phí, vừa bàn lịch họp khách hàng, vừa điều chỉnh ngân sách):
     - **Đan xen đa luồng (Interleaved Threads):** Tin nhắn của chủ đề A, B, C xen kẽ nhau liên tục. LLM thông thường nhồi toàn bộ lịch sử chat vào một prompt dẫn đến ghép nhầm thông tin của dự án A sang dự án B.
     - **Quyết định bị ghi đè theo thời gian (Temporal Overridden State):** Lúc `09:00` Lan chốt lịch họp khách hàng vào `14h Thứ Ba`; đến `09:05` Trưởng phòng báo dời sang `09h Thứ Năm`; `09:06` Lan xác nhận `Thứ Năm`. Khi nhân viên vào sau hỏi `@Agent chốt lịch họp lúc nào?`, các chatbot truyền thống vẫn lấy tin nhắn lúc `09:00` để trả lời sai.
     - **Ảo giác & thiếu bằng chứng đối chiếu (Hallucination):** AI trả lời quy chế hoặc tóm tắt cuộc họp nhưng không chỉ rõ trích từ điều khoản nào trong file PDF hay từ tin nhắn `#msg_id` nào.

---

### 1.3. Hậu quả Hiện hữu nếu không giải quyết (Consequences)
- **Sai lệch quyết định vận hành:** Nhân viên hành động dựa trên thông tin cũ đã bị hủy bỏ trong group chat hoặc do AI tự suy diễn (hallucination) quy chế tài chính/nhân sự.
- **Rủi ro bảo mật & tuân thủ (Compliance Breach):** Lộ tài liệu nhạy cảm giữa các phòng ban trong cùng công ty hoặc rò rỉ dữ liệu giữa các công ty khách hàng (Tenants) trên nền tảng đám mây.
- **Độ trễ cao & lãng phí chi phí Token:** Nhồi toàn bộ lịch sử chat nhóm hỗn độn và toàn bộ kho tài liệu công ty vào prompt khiến chi phí API tăng gấp 3–5 lần và độ trễ vượt quá 10–15 giây/lượt.

---

### 1.4. Vì sao Công cụ Truyền thống Thất bại & Bắt buộc dùng Kiến trúc Đề xuất?

| Giải pháp hiện tại | Ưu điểm | Lý do thất bại trong môi trường Công ty / Tổ chức đa phòng ban |
| :--- | :--- | :--- |
| **ChatGPT / Claude / Gemini (Bản tiêu chuẩn)** | Ngôn ngữ tự nhiên tốt, dùng ngay cho cá nhân. | Không có quản trị Multi-Tenant tập trung; **không có Pre-filtering ACL theo phòng ban** ngay tại tầng Vector DB; không có luồng trình ký HITL nội bộ; dễ lấy nhầm quyết định cũ khi tóm tắt hội thoại đan xen. |
| **Chatbot Kịch bản (Rule-based / Decision Tree)** | Kiểm soát câu trả lời cố định, ít ảo giác. | Đóng cứng vào 1 kịch bản tĩnh; không đọc hiểu được quy chế PDF dài hàng chục trang; **hoàn toàn bất lực trước hội thoại nhóm đan xen tự nhiên**. |
| **Framework Kỹ thuật thuần (LangChain / Dify tự dựng)** | Linh hoạt cho kỹ sư AI. | Giao diện quá phức tạp với Trưởng phòng nghiệp vụ (HR, Kế toán, Marketing); thiếu sẵn cơ chế **Thread Disentanglement**, **Temporal State Tracking (`ACTIVE` vs `OVERRIDDEN`)** và **Adaptive UI Schema** cho nhiều loại hình công ty. |

**=> Lý do bắt buộc dùng kiến trúc của Mini Agent Studio (CHAT-40):** Kết hợp **No-Code Studio + Adaptive Schema Engine** ở tầng giao diện với **Đồ thị trạng thái LangGraph + Pre-filtered Vector RAG 3.072 chiều + Thread Disentanglement & Temporal State Tracking + Chốt chặn HITL/Keycloak SSO** ở tầng lõi.

---

## 2. Chân dung Người dùng, Kịch bản Sử dụng & Phạm vi (Users, Scenarios & Scope)

### 2.1. Phân tách 3 Nhóm Vai trò (3-Tier Role Architecture)
Hệ thống định nghĩa **3 nhóm người dùng** với quyền hạn và điểm chạm giao diện tách biệt hoàn toàn:

1. **Nhóm 1 — Quản trị viên Nền tảng (`SUPER_ADMIN` / Platform Owner):**
   - *Đối tượng:* Đội ngũ vận hành nền tảng SaaS B2B.
   - *Quyền hạn & Nhu cầu:* Khởi tạo không gian làm việc độc lập (`Tenant Provisioning`) cho bất kỳ công ty/tổ chức khách hàng mới; chọn mẫu ngành nghề (`ENTERPRISE`, `EDUCATION`, `HEALTHCARE`, `CUSTOM`); tự động đồng bộ định danh lên **Keycloak OIDC SSO** và gửi mật khẩu quản trị qua **Gmail SMTP**; giám sát tài nguyên toàn hệ thống.
2. **Nhóm 2 — Quản trị viên Công ty / Trưởng Phòng ban (`TENANT_ADMIN` / Unit Manager):**
   - *Đối tượng:* Giám đốc vận hành (COO), Trưởng phòng HR, Trưởng phòng Marketing, Kế toán trưởng tại công ty (hoặc Chủ nhiệm khoa/Giáo vụ ở kịch bản mở rộng).
   - *Quyền hạn & Nhu cầu:* Tự khởi tạo AI Agent cho từng phòng ban không cần code (qua mẫu 1-Click hoặc tự định nghĩa đơn vị mới), upload tài liệu PDF/TXT gán quyền ACL theo phòng ban, bật/tắt Tool kèm Permission Manifest, nhập danh sách nhân sự hàng loạt (CSV) và **phê duyệt/từ chối các đề xuất phát sinh từ luồng HITL**.
3. **Nhóm 3 — Nhân viên / Thành viên Đơn vị (`EMPLOYEE` / Unit Member):**
   - *Đối tượng:* Nhân viên các phòng ban trong công ty (Marketing, Kế toán, HR, IT, Sales...).
   - *Quyền hạn & Nhu cầu:* Chỉ nhìn thấy và tương tác với các Agent thuộc đúng phòng ban của mình (`user.department == agent.department_access`) hoặc Agent toàn công ty (`ALL`); tra cứu quy trình có trích dẫn nguồn, thảo luận nhóm có Agent hỗ trợ tách luồng và gửi yêu cầu phê duyệt (nghỉ phép, duyệt ngân sách, cấp phát...) ngay trong khung chat.

---

### 2.2. Kịch bản Người dùng: Khi nào dùng Chat 1-1 vs. Khi nào dùng Chat Nhóm (Group Chat)?
Hệ thống cung cấp 2 chế độ tương tác bổ trợ chặt chẽ cho nhau trong quy trình làm việc của một công ty:

| Tiêu chí | Kịch bản 1: Chat 1-1 với Agent Đơn vị (`Direct 1-1 Portal`) | Kịch bản 2: Chat Nhóm có Agent điều phối (`Multi-User Group Chat`) |
| :--- | :--- | :--- |
| **Khi nào sử dụng?** | Khi nhân viên cần **tra cứu thông tin cá nhân/quy chế riêng tư** hoặc **khởi tạo đề xuất/đơn từ cá nhân** trình Trưởng phòng. | Khi nhiều thành viên trong cùng phòng ban/dự án **thảo luận song song nhiều đầu việc**, chốt lịch họp, bàn ngân sách và cần `@Agent` tổng hợp hoặc kiểm tra quy định ngay trong luồng bàn bạc. |
| **Ví dụ thực tế tại Công ty** | • Nhân viên Marketing hỏi riêng Agent Marketing về định mức chi phí quảng cáo.<br>• Nhân viên gửi yêu cầu *"Xin nghỉ phép 3 ngày"* hoặc *"Đề xuất duyệt ngân sách chiến dịch TikTok"* qua trạm HITL. | • Nhóm Marketing 4 người vừa bàn kịch bản sự kiện (Luồng 1), vừa đổi lịch họp từ Thứ Ba sang Thứ Năm (Luồng 2), vừa gọi `@Agent tóm tắt các quyết định mới nhất còn hiệu lực và kiểm tra quy định tạm ứng`. |
| **Cơ chế AI cốt lõi kích hoạt** | • Kiểm tra cứng `Unit ACL` (`tenant_id` + `department`).<br>• `Pre-filtered Vector RAG` + trích dẫn tài liệu gốc.<br>• `Tool Calling` + `HITL Interrupt` trình Quản lý duyệt. | • **Thread Disentanglement:** Tách các luồng chủ đề đan xen (`#thread_1`, `#thread_2`).<br>• **Temporal State Tracking:** Lọc bỏ quyết định cũ (`OVERRIDDEN`), chỉ giữ quyết định mới nhất (`ACTIVE`).<br>• **Citation 2 chiều:** Trích dẫn cả mã tin nhắn (`#msg_id`) lẫn tài liệu PDF. |

---

### 2.3. Giới hạn Phạm vi MVP & Phân lớp Trạng thái Triển khai (Scope & Capability Tiers)
Để đảm bảo tính minh bạch tuyệt đối giữa **bản dựng thực tế hiện có trong repo** và **mục tiêu hoàn thiện của đề tài CHAT-40**, phạm vi sản phẩm được gắn nhãn theo 3 mức rõ ràng:
- `✅ Đã có trong bản dựng hiện tại (Implemented in Prototype)`: Đã chạy thực tế end-to-end trong mã nguồn hiện tại.
- `🛠 Cam kết hoàn thiện trong MVP (MVP Target Scope)`: Nằm trong phạm vi cốt lõi của đề tài CHAT-40, đã có thiết kế kiến trúc/dữ liệu và hoàn thiện trong chu kỳ MVP.
- `🚀 Lộ trình Nâng cao (Phase 2 / P1)`: Tính năng mở rộng nâng cao sau MVP.

#### **A. Trong phạm vi MVP (In-Scope):**
1. **Quản trị Multi-Tenant, Adaptive Schema & Định danh SSO:**
   - `✅` Xác thực tập trung qua **Keycloak OIDC/OAuth2 SSO** (`http://localhost:8080`) và tự động gửi mật khẩu qua **Google Gmail SMTP** (`backend/mailer.py`).
   - `✅` **Adaptive UI Schema Engine (`backend/schema_engine.py`):** Tự động biến đổi trường dữ liệu và giao diện theo mọi loại hình công ty (`ENTERPRISE` làm trọng tâm; mở rộng sẵn cho `EDUCATION`, `HEALTHCARE` và sinh tự động bằng AI cho ngành nghề bất kỳ `CUSTOM`).
   - `✅` Quản lý nhân sự theo phòng ban/đơn vị, hỗ trợ thêm lẻ và nhập hàng loạt qua file CSV/TXT.
2. **No-Code Studio Builder & Kho Tri thức Vector RAG:**
   - `✅` Tạo Agent không cần code với 13+ mẫu dựng sẵn hoặc tự định nghĩa phòng ban mới (`__CUSTOM__`); trích xuất PDF nhiều trang ngay trên trình duyệt (`Mozilla PDF.js`), phân mảnh đoạn văn và nhúng Vector **3.072 chiều** (`models/gemini-embedding-001`) kèm **Pre-filtering ACL** theo `tenant_id` và `department_access`.
   - `🛠` Trình kéo thả **Workflow 3–5 Node (React Flow)** (`Input Guard` → `Disentangle/Router` → `RAG/Tool Node` → `HITL Gate` → `Response Synthesis`), cấu hình **≥ 3 MCP-like Tools** (`leave_balance`, `leave_request_create`, `send_email`) kèm **Permission Manifest** và đóng băng phiên bản **Agent Versioning (`v1.0`, `v1.1`)**.
3. **AI Context Core (Xử lý Hội thoại Nhóm) & Phê duyệt HITL:**
   - `✅` **Luồng Phê duyệt Con người (HITL Interrupt):** Tự động chặn các yêu cầu trình ký/đề xuất, lưu trạng thái `PENDING` vào CSDL, hiển thị trên hộp thư Quản trị viên và đẩy thông báo Toast thời gian thực khi được `APPROVED` / `REJECTED`.
   - `🛠` **Group Chat Sandbox (Role Switcher) + Thread Disentanglement + Temporal State Tracking (`ACTIVE` / `OVERRIDDEN` / `CANCELLED` / `DONE`) + Trích dẫn 2 chiều (`#msg_id` & Document Citation Box)**.
4. **Hạ tầng Lưu trữ Kép & Giám sát (Observability):**
   - `✅` Lưu trữ `SQLite 3` tốc độ cao đồng bộ thời gian thực (`AutoSyncSQLiteConnection` trong `backend/mysql_sync.py`) sang **MySQL 8.0 Server** để quan sát trực tiếp trên **MySQL Workbench 8.0 CE**; kèm **X-Ray Telemetry Trace** ngay trên giao diện.
   - `🛠` Tích hợp SDK **Langfuse** thu thập trace phân tán và chạy bộ kiểm thử định lượng tự động (Eval Pipeline).

#### **B. Ngoài phạm vi MVP (Out-of-Scope — Tránh dàn trải):**
- **Không** xây dựng cổng thanh toán trực tuyến (Billing/Subscription Gateway) hay chợ mua bán Agent (Public Marketplace).
- **Không** tích hợp webhook hai chiều vào Zalo, Slack, Microsoft Teams hay Discord thật trong giai đoạn MVP (mọi kịch bản chat 1-1 và chat nhóm đều thực hiện trên Web Portal & Sandbox nội bộ).
- **Không** tự huấn luyện (pre-train) hoặc fine-tune mô hình LLM nền tảng; không xử lý luồng âm thanh/video thời gian thực (chỉ xử lý văn bản, bảng biểu và tài liệu PDF/TXT).

---

### 2.4. Điểm chạm Giao diện Chính (Key UI Touchpoints)
Người dùng tương tác với hệ thống qua **5 điểm chạm giao diện Web** theo phong cách **Clean SaaS Dashboard (OpenDesign Minimalist)**:
1. **SSO Login Gate (`frontend/login.html`):** Cổng đăng nhập 1 nút duy nhất qua Keycloak OIDC SSO.
2. **Super Admin Control Plane (`frontend/super_admin.html`):** Cấp phát công ty/tổ chức mới (`Tenant`), chọn ngành nghề hoặc dùng AI sinh Schema tự động cho bất kỳ lĩnh vực công ty nào.
3. **Tenant Admin & No-Code Studio (`frontend/admin_studio.html`):** Quản lý nhân sự/phòng ban (nhập CSV), thiết kế Agent Split-Screen (Cấu hình ACL, Upload PDF Vector 3072-dim, Workflow Graph, Live Playground kèm X-Ray Trace) và Hộp thư phê duyệt HITL có chuông báo đỏ thời gian thực.
4. **Employee Chat & Group Sandbox Portal (`frontend/employee_portal.html`):** Danh mục Agent tự động mở khóa theo phòng ban của nhân viên (khóa cứng `🔒` các phòng ban khác), khung chat hỗ trợ Citation Box, thẻ xác nhận HITL và chế độ giả lập hội thoại nhóm đa thành viên.
5. **Visual Database Explorer (`frontend/database_viewer.html`):** Trình duyệt trực tiếp 5 bảng CSDL quan hệ phục vụ kiểm tra minh bạch dữ liệu.

---

## 3. Giải pháp Kỹ thuật & Kiến trúc Hệ thống (Technical Solution & System Architecture)

### 3.1. Bảng Khớp nối Công nghệ (Techstack Mapping)
Mọi công nghệ trong hệ thống đều gắn chặt với một nhiệm vụ cụ thể trong luồng xử lý từ đầu vào đến đầu ra:

| Thành phần kỹ thuật | Công nghệ lựa chọn | Vai trò & Nhiệm vụ cụ thể trong luồng xử lý | Trạng thái |
| :--- | :--- | :--- | :---: |
| **1. Frontend UI & Workflow** | HTML5/CSS3/JS (OpenDesign Minimalist), Mozilla `PDF.js`, `React Flow` | Hiển thị SaaS Portal đa vai trò; bóc tách văn bản PDF nhiều trang ngay tại trình duyệt (`PDF.js`); trực quan hóa đồ thị luồng thực thi Agent 3–5 node (`React Flow`). | `✅` UI & PDF.js<br>`🛠` React Flow |
| **2. Backend API Engine** | Python 3.10+, `ThreadingHTTPServer` (`backend/server.py`, tương thích nâng cấp `FastAPI`) | Xử lý RESTful API đa luồng, kiểm soát phiên làm việc, thực thi chốt chặn Unit ACL tại cổng `/api/chat` và điều phối đồng bộ dữ liệu. | `✅` |
| **3. Orchestration Core** | `LangGraph` Architecture (`backend/agent_engine.py`) | Điều phối luồng suy luận theo đồ thị trạng thái (`StateGraph`): phân tách rõ Node định tuyến ý định, Node tách luồng/cập nhật trạng thái, Node RAG/Tool và trạm dừng `HITL Interrupt`. | `✅` 2-Node Core<br>`🛠` 5-Node Graph |
| **4. LLM & Embedding Gateway** | Google `gemini-flash-latest` (`temp=0.2`), `models/gemini-embedding-001` (3072-dim) | Sinh phản hồi bám sát ngữ cảnh (`temp=0.2` chống ảo giác), phân loại ý định/biên hội thoại và nhúng văn bản thành vector 3.072 chiều độ chính xác cao. | `✅` |
| **5. Vector Store & Pre-filter** | Custom JSON Vector Engine (`backend/vector_store.py` - Cosine Index) | Lưu trữ vector 3.072 chiều và thực thi **Pre-retrieval Metadata Filtering** theo `tenant_id` + `department_access` trước khi tính Cosine Similarity (`> 0.35`). | `✅` |
| **6. Dual Relational DB** | `SQLite 3` (`database.db`) + `MySQL 8.0 Server` (`backend/mysql_sync.py`) | Lưu trữ giao dịch tốc độ cao trên SQLite và tự động nhân bản tức thì mọi lệnh `INSERT/UPDATE/DELETE` (`AutoSyncSQLiteConnection`) sang MySQL 8.0 để giám sát qua **MySQL Workbench**. | `✅` |
| **7. Identity & Credential Delivery** | `Keycloak OIDC SSO` (OAuth2/JWT, cổng `8080`) + `Google Gmail SMTP` (`backend/mailer.py`) | Quản lý định danh tập trung chuẩn Enterprise (Realm `mini-agent-platform`); tự động tạo user trên Keycloak và gửi email bàn giao mật khẩu ngẫu nhiên an toàn. | `✅` |
| **8. Adaptive Domain Engine** | `Schema Engine` (`backend/schema_engine.py`) | Tự động cấu hình trường hồ sơ nhân sự, đơn vị và biểu mẫu HITL cho bất kỳ ngành nghề công ty nào (`ENTERPRISE`, `EDUCATION`, `HEALTHCARE`, `CUSTOM`). | `✅` |
| **9. Tool Execution Layer** | MCP-like Tool Registry & Permission Manifest | Chuẩn hóa giao tiếp các công cụ nghiệp vụ (`leave_balance`, `leave_request_create`, `send_email`), kiểm tra quyền `read/write/sensitive` trước khi chạy. | `✅` HITL Tool<br>`🛠` ≥ 3 MCP Tools |
| **10. Observability & Eval** | Built-in `X-Ray Telemetry Trace` + `Langfuse SDK` | Ghi nhận thời gian thực `intent`, `latency_ms`, `token_estimate`, `cosine_score` trên UI và đẩy log chấm điểm tự động lên Langfuse. | `✅` X-Ray UI<br>`🛠` Langfuse SDK |

---

### 3.2. Giải quyết các Nút thắt Kỹ thuật Khó (Core Algorithmic Mechanisms)

#### **A. Cơ chế Tách luồng Hội thoại Đan xen (Hybrid Thread Disentanglement — 3 bước)**
Để giải quyết bài toán nhiều nhân viên nói chuyện xen kẽ nhiều chủ đề trong một phòng chat chung, hệ thống xử lý theo chuỗi 3 bước:
```text
[Tin nhắn mới m_i] 
   ──► Bước 1: Heuristic & Metadata Anchor (Reply-to, @Mention, Time Window Δt ≤ 5 phút)
   ──► Bước 2: Semantic Clustering (Cosine Similarity giữa Vector 3072-dim của m_i và Centroid các Thread đang mở)
   ──► Bước 3: LLM Boundary Adjudicator (Chỉ gọi Gemini Flash khi điểm tương đồng nằm vùng biên 0.45 ≤ sim ≤ 0.65)
   ──► Gán nhãn thread_id & Cập nhật Context riêng của Thread đó
```
- **Bước 1 (Tín hiệu cấu trúc):** Nếu tin nhắn có `reply_to_msg_id` hoặc `@mention` trực tiếp một thành viên trong luồng vừa tương tác dưới 5 phút, gán thẳng vào `thread_id` tương ứng với độ trễ $\approx 0\text{ ms}$.
- **Bước 2 (Gom cụm ngữ nghĩa):** Tính tích vô hướng Cosine giữa vector nhúng của tin nhắn mới với vector trọng tâm (Centroid) của các luồng đang hoạt động trong cửa sổ trượt. Nếu $\text{sim} > 0.65$, gộp vào luồng có điểm cao nhất; nếu $\text{sim} < 0.45$, khởi tạo luồng chủ đề mới.
- **Bước 3 (Phân xử vùng biên bằng LLM):** Chỉ những tin nhắn mơ hồ ($0.45 \le \text{sim} \le 0.65$) mới gọi LLM phân xử nhẹ, giúp tiết kiệm tối đa lượt gọi LLM mà vẫn giữ điểm F1 tách luồng cao.

#### **B. Cơ chế Theo dõi Trạng thái Quyết định theo Thời gian (Temporal State Tracking)**
Mỗi quyết định, lịch hẹn, phân công hoặc chốt số liệu trong hội thoại được trích xuất thành bản ghi `DecisionState` có máy trạng thái hữu hạn (FSM):
```text
[NEW DECISION] ──► ACTIVE (Đang có hiệu lực)
                     ├──► OVERRIDDEN (Bị thay thế bởi quyết định mới hơn: superseded_by = #msg_new)
                     ├──► CANCELLED  (Bị hủy bỏ明确 bởi người có thẩm quyền)
                     └──► DONE       (Đã hoàn thành thực thi)
```
- Khi phát hiện tin nhắn mới có thực thể cùng chủ đề (`topic_key`, ví dụ: `"Lịch họp khách hàng tuần này"`) nhưng mang giá trị cập nhật hoặc phủ định (ví dụ: *"Dời lịch họp Thứ 3 sang 9h Thứ 5 nhé"*), hệ thống tự động chuyển bản ghi cũ sang `OVERRIDDEN`, lưu con trỏ `superseded_by = msg_id_mới`, và tạo bản ghi mới ở trạng thái `ACTIVE`.
- **Quy tắc chống dùng thông tin cũ (Zero Stale-Decision Rule):** Khi người dùng hỏi tiến độ hoặc yêu cầu tóm tắt, bộ truy xuất **chỉ nạp các bản ghi có `state == ACTIVE`** (kèm lịch sử thay đổi nếu được hỏi lý do), triệt tiêu hoàn toàn lỗi lấy quyết định cũ đã hủy để trả lời.

#### **C. Tiền lọc Vector Đa tầng (2-Layer Pre-retrieval Vector Filtering)**
Thay vì tìm kiếm Top-K trên toàn bộ kho vector rồi mới lọc quyền (Post-filtering — dễ dẫn đến rỗng kết quả hoặc lộ thông tin qua điểm số), `backend/vector_store.py` thực thi **Pre-filtering** ngay trước phép nhân ma trận Cosine:
1. **Lọc cứng Tầng 1 (`tenant_id`):** Chỉ giữ các vector thuộc đúng công ty đang đăng nhập.
2. **Lọc cứng Tầng 2 (`department_access`):** Chỉ giữ các tài liệu có nhãn `ALL` (toàn công ty) hoặc trùng khớp chính xác với `user.department` của người hỏi.
3. **Ngưỡng từ chối an toàn (`Cosine Threshold > 0.35`):** Chỉ những đoạn văn vượt ngưỡng tương đồng `0.35` mới được đưa vào Prompt kèm định danh nguồn `[Tài liệu: <file_name> | Độ khớp: <score>]`.

---

### 3.3. Lợi thế Kiến trúc (Architectural Advantages)
1. **Tối ưu chi phí Token & Độ trễ phản hồi (P95 $< 3.0\text{s}$):** Nhờ tách nhỏ quy trình thành các Node chuyên biệt trên LangGraph, tiền lọc Vector theo đơn vị và chỉ nạp đúng các tin nhắn cùng `thread_id` + trạng thái `ACTIVE` vào Prompt, hệ thống loại bỏ được phần lớn dữ liệu nhiễu không liên quan, giữ độ trễ phản hồi đơn lượt ổn định dưới 3 giây và tiết kiệm chi phí gọi API LLM.
2. **Mở rộng sang bất kỳ ngành nghề công ty nào trong vài giây (Zero-Code Domain Adaptation):** Kiến trúc tách rời hoàn toàn **Lõi điều phối AI (`agent_engine.py`)** khỏi **Cấu trúc hiển thị ngành nghề (`schema_engine.py`)**. Khi một công ty thuộc lĩnh vực mới (ví dụ: Công ty Logistics, Chuỗi Bán lẻ, Ngân hàng hay Trường học) đăng ký sử dụng, hệ thống tự động sinh bộ thuộc tính (`ui_schema`) phù hợp mà không cần sửa bất kỳ dòng code Backend hay Database nào.
3. **An toàn cho cả Môi trường Thử nghiệm & Quản trị Doanh nghiệp:** Kiến trúc CSDL kép (`SQLite` nội bộ + đồng bộ tự động `MySQL 8.0`) giúp ứng dụng khởi chạy nhẹ nhàng ngay lập tức nhưng vẫn cho phép đội ngũ IT/Ban Giám Khảo dùng công cụ chuẩn doanh nghiệp (**MySQL Workbench 8.0 CE** & **Keycloak Admin Console**) để kiểm tra trực tiếp.

---

## 4. Dữ liệu, Bảo mật & Ràng buộc Thực thi (Data, Security & Governance)

### 4.1. Kiểm soát Truy cập 3 Tầng (3-Layer Access Control)
1. **Tầng Định danh (Identity Layer — Keycloak OIDC SSO):** Mọi người dùng bắt buộc đăng nhập qua máy chủ Keycloak (`Realm: mini-agent-platform`). Hệ thống đối chiếu email/token đã xác thực với hồ sơ nội bộ để lấy đúng bộ khóa `(tenant_id, role, department)`, tuyệt đối không cho phép client tự giả mạo quyền ở giao diện.
2. **Tầng Cổng API (API Route Guardrail):** Tại endpoint `/api/chat`, trước khi khởi tạo LLM, hệ thống kiểm tra điều kiện cứng: nếu `agent.department_access != 'ALL'` và `user.department != agent.department_access` (đối với `EMPLOYEE`), hệ thống lập tức chặn truy cập và trả về mã lỗi `ACL_DENIED` trong $< 0.05\text{ giây}$.
3. **Tầng Lưu trữ Vector & Quan hệ (Storage Layer Pre-filtering):** Mọi truy vấn SQL và Vector Search đều bắt buộc gắn mệnh đề lọc `WHERE tenant_id = ?` và `department_access IN ('ALL', ?)`, đảm bảo cô lập dữ liệu 100% giữa các công ty và giữa các phòng ban.

### 4.2. Kiểm soát Rủi ro Thực thi & Chốt chặn Con người (HITL & Tool Manifest)
- **Phân loại rủi ro công cụ (Permission Manifest):** Mỗi Tool gắn vào Agent được khai báo mức độ rủi ro:
  - `read-only` (An toàn — thực thi tự động): Ví dụ `leave_balance` (tra cứu số ngày phép/định mức còn lại).
  - `sensitive-write` (Nhạy cảm — bắt buộc qua HITL): Ví dụ `leave_request_create` (tạo đơn nghỉ phép/đề xuất ngân sách/yêu cầu mua sắm), `send_email` (gửi thông báo chính thức).
- **Trạm dừng phê duyệt (`HITL Interrupt`):** Khi Agent phát hiện yêu cầu thuộc nhóm `sensitive-write`, `LangGraphAgent` kích hoạt cờ `interrupt_hitl = True`, dừng việc thực thi tự động và trả về **Thẻ Xác nhận Phê duyệt** trên giao diện chat. Chỉ khi người dùng xác nhận và Quản trị viên đơn vị (`TENANT_ADMIN`) bấm **`[Duyệt (Approve)]`** trên hộp thư quản trị, trạng thái mới chuyển từ `PENDING` sang `APPROVED` và bắn thông báo Toast thời gian thực về cho nhân viên.

### 4.3. Khả năng Truy vết Toàn diện (End-to-End Traceability & Citation)
- **Trích dẫn nguồn 2 chiều (Dual Citation Grounding):**
  - *Với tài liệu quy chế (RAG):* Hiển thị rõ tên file PDF/TXT gốc, đoạn văn bản trích xuất và điểm số tương đồng Cosine Similarity.
  - *Với thảo luận nhóm (Chat Context):* Liên kết ngược về mã định danh tin nhắn gốc (`#msg_id`), người gửi và mốc thời gian đưa ra quyết định.
- **Nhật ký thực thi X-Ray & Audit Log:** Mọi lượt hội thoại đều trả về đối tượng `trace` ghi rõ: `intent` đã nhận diện, trạng thái kiểm tra `ACL`, danh sách `chunks` hoặc `tool` đã gọi, thời gian xử lý (`latency_ms`), lượng `token_estimate` và lưu lịch sử duyệt đơn vào bảng `leave_requests` trên cả SQLite và MySQL 8.0.

---

## 5. Chỉ số Thành công & Bộ Đo lường (Success Metrics & Evaluation Benchmarks)

### 5.1. Bảng Chỉ số Định lượng Mục tiêu (Quantitative KPIs)

| Nhóm chỉ số | Tên thước đo (Metric) | Ngưỡng mục tiêu MVP (Target) | Phương pháp đo lường |
| :--- | :--- | :--- | :--- |
| **1. Bảo mật & Phân quyền** | **Unit ACL & Tenant Isolation Rate** | **100%** (0% rò rỉ dữ liệu chéo) | Chạy bộ $\ge 50$ kịch bản Red-team truy vấn vượt quyền giữa các phòng ban/công ty. |
| **2. Kiểm soát Rủi ro** | **HITL Interception Accuracy** | **100%** tác vụ nhạy cảm bị chặn chờ duyệt | Kiểm thử các lệnh tạo đề xuất/đơn từ/gửi email; 0% lệnh tự ý thực thi ngầm. |
| **3. Xử lý Hội thoại Nhóm** | **Thread Disentanglement Micro-F1** | **$\ge 0.72$** (Cơ sở) / **$\ge 0.85$** (Mục tiêu) | Đánh giá F1 phân cụm chủ đề trên tập hội thoại nhóm đan xen 3–5 luồng song song. |
| **4. Trạng thái Thời gian** | **Temporal State Accuracy & Stale Rate** | Accuracy **$\ge 80\%$**, Stale Usage **$\le 5\%$** | Đo tỷ lệ Agent trả lời đúng quyết định `ACTIVE` mới nhất và không dùng lại tin nhắn `OVERRIDDEN`. |
| **5. Độ trung thực RAG** | **Citation Faithfulness & Coverage** | Faithfulness **$\ge 90\%$**, Coverage **$\ge 95\%$** | Đối chiếu câu trả lời của Agent với đoạn trích trong PDF/tin nhắn nguồn (`#msg_id`). |
| **6. Hiệu năng & Vận hành** | **End-to-End Response Latency** | **P50 $\le 1.5\text{s}$, P95 $< 3.0\text{s}$** (đơn lượt)<br>**P95 $< 8.0\text{s}$** (tóm tắt đa luồng) | Đo trực tiếp qua bộ đếm `latency` của X-Ray Telemetry Trace và Langfuse. |
| **7. Trải nghiệm No-Code** | **Time-to-Publish New Unit Agent** | **$< 3\text{ phút}$** cho mỗi phòng ban mới | Đo thời gian từ lúc Admin chọn mẫu/tạo phòng ban, nạp file PDF đến khi Publish xong Agent. |

---

### 5.2. Tập Dữ liệu Kiểm chứng Chuẩn (Evaluation Benchmark Datasets)
Hệ thống kết hợp các bộ dữ liệu chuẩn quốc tế và bộ kịch bản tiếng Việt chuyên biệt cho môi trường công ty:
1. **Ubuntu Chat Disentanglement Dataset (Kummerfeld et al.):** Dùng để chuẩn hóa và đo kiểm thuật toán tách luồng hội thoại đan xen (chỉ số Micro-F1, Shen-F1).
2. **SAMSum / DialogSum & MeetingBank:** Dùng để kiểm chứng khả năng tóm tắt hội thoại nhiều người tham gia và trích xuất quyết định cuộc họp không sinh ảo giác.
3. **MultiWOZ / $\tau$-bench (Tool-Agent-User Interaction Benchmark):** Dùng để đánh giá độ chính xác khi lựa chọn công cụ (Tool Calling) và tuân thủ chính sách phê duyệt nhiều bước.
4. **Bộ dữ liệu Nội bộ Đa ngành Tiếng Việt (`CHAT40-VN-Enterprise-Eval` — $\ge 100$ kịch bản):**
   - **50 kịch bản Red-team ACL & Multi-Tenant:** Nhân viên phòng Marketing cố tình hỏi dữ liệu Kế toán/HR, hoặc người dùng công ty A truy vấn dữ liệu công ty B.
   - **30 kịch bản Hội thoại Nhóm Đan xen & Ghi đè Thời gian (Temporal Override):** Các cuộc thảo luận phòng ban có 3–4 chủ đề xen kẽ, trong đó lịch họp, ngân sách và người phụ trách bị thay đổi 2–3 lần liên tiếp.
   - **20 kịch bản Quy chế PDF & Trình duyệt HITL đa ngành:** Bao phủ kịch bản trọng tâm Doanh nghiệp (`VinFast`, `FPT`) và các kịch bản mở rộng Giáo dục (`ĐHQG`), Y tế (`BVQT`).

---

### 5.3. Công cụ Giám sát & Đánh giá Tự động (Observability & Monitoring Stack)
- **X-Ray Telemetry Trace (Tích hợp sẵn trên UI):** Hiển thị trực tiếp ở cột phải của Studio Playground và bảng Thống kê AI Chat (`#tab-analytics`), cho phép theo dõi tức thì: `Intent Classification`, `ACL Check Status`, `Retrieved Vector Chunks & Cosine Score`, `Latency (ms)` và `Estimated Tokens`.
- **Langfuse Observability Platform:** Ghi nhận toàn bộ chuỗi thực thi (Trace/Span) của từng Node trong LangGraph, thống kê chi phí token theo từng Công ty (`tenant_id`) / Phòng ban (`department`), và chạy hàm chấm điểm tự động (*LLM-as-a-Judge* cho Faithfulness & Relevancy).

---

## 6. Sản phẩm Đầu ra & Tính Khả thi (Deliverables & Packaging)

### 6.1. Danh mục Sản phẩm Bàn giao (Deliverables Checklist)
1. **Mã nguồn Ứng dụng Full-Stack (`backend/` & `frontend/`):**
   - **Backend (`backend/`):** Máy chủ API đa luồng (`server.py`), Lõi điều phối `LangGraphAgent` (`agent_engine.py`), Kho Vector 3.072 chiều có Pre-filtering ACL (`vector_store.py`), Động cơ giao diện thích ứng mọi loại hình công ty (`schema_engine.py`), Bộ đồng bộ thời gian thực SQLite → MySQL 8.0 (`mysql_sync.py`), Dịch vụ gửi email mật khẩu tự động (`mailer.py`), và Bộ khởi tạo dữ liệu mẫu đa ngành (`database.py`, `seed_multi_tenant.py`).
   - **Frontend (`frontend/`):** 5 phân hệ giao diện hoàn chỉnh (`login.html`, `super_admin.html`, `admin_studio.html`, `employee_portal.html`, `database_viewer.html`).
2. **Cơ sở Dữ liệu & Kho Tri thức Mẫu:**
   - File CSDL `backend/database.db` (SQLite) và bản dump `backend/mysql_workbench_export.sql` (chuẩn MySQL 8.0) chứa sẵn 4 tổ chức mẫu (`VINFAST`, `FPT`, `VNU`, `BVQT`), 15+ tài khoản phân quyền, 12+ Agent chuyên biệt và các tài liệu quy chế đã nhúng sẵn vector 3.072 chiều trong `backend/vector_store.json`.
3. **Bộ Tài liệu Thiết kế & Nghiệm thu Chuẩn hóa:**
   - Bản Tuyên bố Bài toán & Kiến trúc (`Brief.md` & `Brief_CHAT_40_Mini_Agent_Studio.docx`).
   - Tài liệu Yêu cầu Sản phẩm 7 phần (`PRD.md` & `PRD_Mini_Agent_Studio_CHAT40.docx`).
   - Tài liệu Thiết kế Giao diện & Luồng Màn hình (`Wireframe_UI_Flow.md`).
   - Nhật ký Ứng dụng AI & Thực nghiệm (`AI_Log.md`) và Hướng dẫn Cài đặt & Kiểm thử (`README.md`).

---

### 6.2. Khả năng Đóng gói & Khởi chạy Đồng nhất (Reproducible Deployment)
Hệ thống được thiết kế theo cơ chế **Graceful Degradation (Tự động thích ứng môi trường)** để Ban Giám Khảo hoặc Khách hàng có thể khởi chạy kiểm thử ngay lập tức ở cả **2 chế độ**:

1. **Chế độ Khởi chạy Nhanh 1 Lệnh (Standalone Quick-Start — Không cần cài đặt dịch vụ ngoài):**
   - Chỉ cần Python 3.10+ và chạy lệnh duy nhất:
     ```bash
     python backend/server.py
     ```
   - Hệ thống tự động nạp CSDL `SQLite` nội bộ và kho `vector_store.json` đã nhúng sẵn vector 3.072 chiều, mở cổng `http://localhost:8000` để kiểm thử ngay lập tức các luồng phân quyền Unit ACL, RAG Citation và duyệt đơn HITL.
2. **Chế độ Full Enterprise Production (Keycloak SSO + Gmail SMTP + MySQL 8.0 Workbench):**
   - Khởi chạy máy chủ định danh **Keycloak OIDC** qua Docker (`docker run -p 8080:8080 ...` kèm lệnh `python setup_keycloak.py` tự động tạo Realm `mini-agent-platform` và đồng bộ toàn bộ tài khoản).
   - Cấu hình biến môi trường `.env` (`GEMINI_API_KEY`, `SMTP_USER`, `SMTP_PASSWORD`, `MYSQL_PASSWORD`) để trải nghiệm trọn vẹn luồng: **Tạo công ty mới bằng Gmail thật → Tự động nhận email mật khẩu → Đăng nhập SSO → Đồng bộ tức thì sang MySQL Workbench 8.0 CE**.
