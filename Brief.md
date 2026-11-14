# PROJECT BRIEF: MINI AGENT STUDIO (CHAT-40)

* **Tên đề tài:** Mini Agent Studio — Nền tảng No-Code khởi tạo AI Agent đa lĩnh vực, xử lý đan xen hội thoại & phân quyền theo đơn vị (Phòng ban / Khoa / Lớp học)
* **Mã đề tài:** CHAT-40
* **Nhóm thực hiện:** AI20K - Team T057 (CHAT-40)
* **Phiên bản:** v2.0 (Chuẩn hóa theo cấu trúc Product Discovery Brief)

---

## 1. Background — Bối cảnh & Thực trạng

Trong kỷ nguyên chuyển đổi số, nhu cầu triển khai Trợ lý ảo AI (AI Agent) để tự động hóa quy trình, giải đáp quy chế và hỗ trợ tác vụ chuyên môn đang bùng nổ ở **mọi lĩnh vực và mô hình tổ chức**:
* **Khối Doanh nghiệp (Enterprise):** Cần các Agent chuyên trách cho từng **Phòng ban** (*Phòng Marketing, Phòng Kế toán - Tài chính, Phòng Nhân sự - HR, Phòng Kỹ thuật - IT, Phòng Kinh doanh - Sales...*).
* **Khối Giáo dục & Đào tạo (Education):** Cần các Agent chuyên trách cho từng **Khoa / Viện / Lớp học / Phòng chức năng** (*Trợ giảng Lớp AI/CNTT, Cố vấn Khoa Kinh tế, Agent Phòng Đào tạo & Học vụ, Phòng Công tác Sinh viên, Thư viện...*).
* **Khối Y tế & Tổ chức (Healthcare & Organizations):** Cần các Agent hỗ trợ theo từng **Chuyên khoa / Bộ phận** (*Khoa Khám bệnh, Khoa Dược, Hành chính tổng hợp...*).

Tuy nhiên, quá trình đưa AI Agent từ thử nghiệm vào vận hành thực tế tại các tổ chức đang vấp phải **3 nhóm khó khăn cốt lõi**:

### A. Khó khăn trong tiếp cận & khởi tạo AI Agent theo đơn vị (Technical & Domain Barrier)
* **Rào cản kỹ thuật đối với người nắm nghiệp vụ:** Các Trưởng phòng ban (Marketing, Kế toán, HR), Giáo vụ khoa hay Giảng viên chủ nhiệm lớp là những người hiểu rõ nhất quy trình, tài liệu và nhu cầu của đơn vị mình nhưng **không có kỹ năng lập trình (Coding)** để tự cấu hình Prompt, gắn kho tài liệu (Vector RAG) hay thiết lập công cụ (Tools) cho AI.
* **Sự đóng cứng và manh mún của các chatbot truyền thống:** Các giải pháp chatbot hiện hữu thường bị khóa cứng vào một kịch bản đơn lẻ (ví dụ: chỉ trả lời FAQ tĩnh hoặc chỉ tính ngày nghỉ phép), đòi hỏi đội ngũ IT phải viết code lại từ đầu mỗi khi muốn triển khai thêm Agent cho một phòng ban mới, một lớp học mới hay một lĩnh vực mới.

### B. Khó khăn trong quản lý, phân quyền dữ liệu & kiểm soát rủi ro (Governance & Security)
* **Nguy cơ rò rỉ dữ liệu chéo giữa các đơn vị (Lack of Unit Isolation):** Trong một tổ chức, mỗi đơn vị sở hữu kho tài liệu nhạy cảm riêng (ví dụ: báo cáo ngân sách của *Phòng Kế toán*, chiến lược chiến dịch của *Phòng Marketing*, hay đề cương/hồ sơ học vụ của *Phòng Đào tạo*). Các công cụ AI dùng chung hiện nay thiếu cơ chế phân quyền đa tầng (`Tenant -> Đơn vị/Phòng ban/Lớp học`), dẫn đến rủi ro nhân viên phòng này hoặc sinh viên lớp khác truy xuất trái phép dữ liệu mật.
* **Thiếu cơ chế kiểm soát của con người đối với tác vụ nhạy cảm (Lack of Human-in-the-Loop - HITL):** Khi thành viên yêu cầu AI thực hiện các tác vụ có tính cam kết (như trình duyệt ngân sách Marketing, nộp đơn học vụ/hoãn thi, yêu cầu cấp phát thiết bị), việc để AI tự động thực thi 100% mà không qua trạm phê duyệt của Quản lý / Ban chủ nhiệm đơn vị tiềm ẩn rủi ro vận hành rất lớn.

### C. Khó khăn trong vận hành thực tế & xử lý ngữ cảnh hội thoại (Operational & Context Chaos)
* **Hội thoại đan xen đa chủ đề (Interleaved Multi-Thread Chaos):** Khác với môi trường chat 1-1 đơn tuyến, trong không gian làm việc thực tế của phòng ban hoặc lớp học, các thành viên thường trao đổi đan xen nhiều chủ đề cùng lúc (vừa hỏi quy trình thanh toán, vừa bàn kế hoạch tuần, vừa xin phê duyệt đề xuất). Các LLM thông thường dễ bị "nhiễu ngữ cảnh" (*Context Pollution*), ghép nhầm thông tin của luồng này sang luồng khác.
* **Trạng thái thông tin thay đổi liên tục theo thời gian (Temporal Overridden State):** Các quyết định trong cuộc họp hoặc nhóm làm việc thường xuyên bị cập nhật, đính chính hoặc hủy bỏ bởi các tin nhắn sau đó (ví dụ: thay đổi lịch học, điều chỉnh hạn nộp báo cáo). AI truyền thống không phân biệt được thông tin nào còn hiệu lực và thông tin nào đã bị ghi đè.
* **Hiện tượng ảo giác & thiếu bằng chứng đối chiếu (Hallucination & Lack of Citation):** AI thường tự suy diễn quy chế hoặc trả lời chung chung mà không trích dẫn rõ nguồn văn bản nội bộ hay tin nhắn gốc, khiến người dùng không dám tin tưởng để ra quyết định.

---

## 2. Current Alternatives & Limitations — Giải pháp hiện tại & Hạn chế

| Giải pháp hiện tại | Ưu điểm | Hạn chế lớn đối với bài toán Tổ chức Đa đơn vị |
| :--- | :--- | :--- |
| **ChatGPT / Claude / Gemini (Bản tiêu chuẩn)** | Khả năng ngôn ngữ mạnh, dễ dùng cho cá nhân. | Không có quản trị Multi-Tenant tập trung, không có phân quyền cứng theo Phòng ban / Lớp học (Unit ACL), không có luồng duyệt đơn HITL nội bộ. |
| **Chatbot kịch bản (Rule-based / Decision Tree)** | Kiểm soát câu trả lời cố định, không bị ảo giác. | Cứng nhắc, không hiểu ngôn ngữ tự nhiên phức tạp, không thể đọc hiểu tài liệu PDF/quy chế dài hoặc tách luồng hội thoại đan xen. |
| **Các nền tảng Agent kỹ thuật (LangChain / Dify tự dựng)** | Linh hoạt cho lập trình viên. | Giao diện quá phức tạp với Quản lý bộ phận / Giáo vụ không chuyên IT; thiếu sẵn cơ chế tiền lọc Vector theo đơn vị (Pre-filtering ACL) và đánh giá định lượng tách luồng hội thoại. |

---

## 3. Target Users — Người dùng mục tiêu

Hệ thống **Mini Agent Studio (CHAT-40)** phục vụ 3 nhóm người dùng mục tiêu rõ rệt tương ứng với mô hình phân quyền 3 tầng:

### 3.1. Nhóm 1: Quản trị viên Tổ chức / Trưởng bộ phận / Giáo vụ (Tenant Admin & Unit Creator)
* **Đại diện:** Giám đốc vận hành, Trưởng phòng Nhân sự/Marketing/Kế toán tại Doanh nghiệp; Cán bộ Phòng Đào tạo, Chủ nhiệm Khoa, Giảng viên phụ trách lớp tại Trường học.
* **Nhu cầu (Needs):**
  * Tự khởi tạo nhanh các AI Agent chuyên trách cho từng **Phòng ban / Khoa / Lớp học** bằng giao diện kéo-thả / chọn mẫu (No-Code) chỉ trong vài phút.
  * Tải lên tài liệu quy chế, giáo trình, hướng dẫn nghiệp vụ (PDF, TXT, MD) để AI tự động vector hóa và đóng khung phạm vi truy cập theo đúng đơn vị.
  * Quản lý danh sách thành viên (thêm lẻ hoặc nhập hàng loạt qua CSV), phân bổ thành viên vào từng Đơn vị/Lớp/Phòng ban và phê duyệt các đề xuất phát sinh từ luồng **HITL**.

### 3.2. Nhóm 2: Thành viên / Nhân viên / Giảng viên / Sinh viên (End-Users / Unit Members)
* **Đại diện:** Nhân viên các phòng ban (Marketing, Kế toán, IT, Sales...), Sinh viên các lớp học, Bác sĩ/Nhân viên y tế tại các chuyên khoa.
* **Nhu cầu (Needs):**
  * Truy cập đúng Trợ lý AI thuộc đơn vị của mình để hỏi đáp quy trình, tra cứu tài liệu chuyên môn hoặc bài giảng 24/7 với **trích dẫn nguồn chính xác**.
  * Khởi tạo nhanh các yêu cầu/đề xuất nghiệp vụ (đề xuất chiến dịch, đơn xin học vụ, phiếu yêu cầu hỗ trợ...) ngay trong khung chat để trình Quản lý duyệt và nhận thông báo kết quả theo thời gian thực.

### 3.3. Nhóm 3: Quản trị viên Nền tảng (Platform Super Admin)
* **Đại diện:** Đội ngũ vận hành nền tảng SaaS B2B (Mini Agent Studio).
* **Nhu cầu (Needs):**
  * Cấp phát bản quyền và khởi tạo không gian làm việc độc lập (Tenant Provisioning) cho các Doanh nghiệp, Trường học, Bệnh viện mới.
  * Giám sát tài nguyên, quản lý đồng bộ định danh SSO (Keycloak) và theo dõi chỉ số chất lượng suy luận AI (Latency, Token, Accuracy) trên toàn hệ thống.

---

## 4. Initial Problem Statement — Phát biểu bài toán

> **"Làm thế nào để chúng ta (How Might We)** xây dựng một nền tảng **No-Code AI Agent Studio đa lĩnh vực** giúp Quản trị viên của bất kỳ tổ chức nào (Doanh nghiệp, Trường học, Y tế) có thể tự khởi tạo và phân quyền các Trợ lý AI chuyên biệt theo từng **Đơn vị (Phòng ban / Khoa / Lớp học)** chỉ trong vài phút — đồng thời đảm bảo AI có khả năng **phân tách đúng các luồng hội thoại đan xen**, **loại bỏ thông tin cũ đã bị ghi đè theo thời gian**, **trích dẫn chính xác nguồn tri thức nội bộ** và **tuân thủ tuyệt đối ranh giới bảo mật dữ liệu (RBAC/ACL & Human-in-the-Loop)**?"

---

## 5. Desired Outcomes — Kết quả kỳ vọng (Mục tiêu định lượng & định tính)

### 5.1. Kết quả kỳ vọng về Trải nghiệm & Nghiệp vụ (Business & UX Outcomes)
1. **Khởi tạo Agent Đa ngành nghề siêu tốc (Time-to-Value < 3 phút):**
   * Admin không biết lập trình có thể sử dụng bộ **13+ Mẫu Agent Đa lĩnh vực (1-Click Templates)** (Phòng Marketing, Kế toán, HR, IT, Sales; Lớp AI/CNTT, Phòng Đào tạo, Khoa Kinh tế, CTSV, Thư viện; Khoa Khám bệnh, Khoa Dược...) hoặc tự định nghĩa tên Lớp / Phòng ban mới để xuất bản Agent ngay lập tức.
2. **Cô lập dữ liệu tuyệt đối giữa các Tổ chức & Đơn vị (100% Isolation):**
   * Thành viên thuộc đơn vị nào (ví dụ: `Marketing` hoặc `Lớp AI - K68`) chỉ được phép tương tác và truy xuất tri thức của đơn vị đó (cùng các Agent toàn tổ chức `ALL`). Mọi truy cập trái phép sang đơn vị khác đều bị chặn tự động bởi lớp bảo vệ **RBAC & Unit ACL Guardrail**.
3. **Chuẩn hóa quy trình Trình ký & Phê duyệt (100% HITL Governance):**
   * Mọi yêu cầu tạo đề xuất/đơn từ trong hội thoại đều tự động kích hoạt trạm dừng **HITL**, lưu vào CSDL và đẩy thông báo hai chiều thời gian thực giữa Thành viên và Quản trị viên.

### 5.2. Kết quả kỳ vọng về Kỹ thuật & Chất lượng AI (Technical & Evaluation KPIs)
* **Độ chính xác tách luồng hội thoại (Thread Disentanglement):** Đạt $\text{Micro-F1} \ge 0.72$ trên bộ dữ liệu kiểm thử hội thoại đan xen.
* **Theo dõi trạng thái thời gian (Temporal State Tracking):** Phát hiện chính xác $\ge 80\%$ các quyết định/thông tin đã bị thay đổi hoặc hủy bỏ (`OVERRIDDEN`), không đưa thông tin cũ vào bản tóm tắt cuối.
* **Độ trung thực & Trích dẫn nguồn (Citation Faithfulness):** $\ge 90\%$ câu trả lời của Agent gắn kèm trích dẫn chính xác tên tài liệu quy chế/giáo trình và độ tương đồng ngữ nghĩa (Cosine Similarity).
* **Hiệu năng phản hồi (System Latency):** Thời gian phản hồi trung bình (P95) từ lúc gửi tin nhắn đến khi nhận câu trả lời đạt $< 3\text{ giây}$.

---

## 6. Product Opportunity — Cơ hội sản phẩm & Giải pháp (Mini Agent Studio)

Để hiện thực hóa các kết quả kỳ vọng trên, **Mini Agent Studio (CHAT-40)** được thiết kế theo kiến trúc **"Chia để trị" (Divide & Conquer)** với 4 trụ cột sản phẩm:

### 6.1. Giao diện Quản trị & No-Code Studio Đa Lĩnh Vực (SaaS Dashboard UI)
* **Thiết kế trực quan, hiện đại:** Bố cục chuẩn SaaS Portal gồm Thanh điều hướng dọc (Sidebar), Thẻ tổng quan tổ chức, Thanh chuyển đổi Sub-tab và Cổng kiểm thử trực tiếp (**Agent Live Playground**).
* **Quản lý Thành viên & Đơn vị linh hoạt:** Hỗ trợ thêm thành viên đơn lẻ hoặc nhập hàng loạt từ file CSV/TXT, tự động đồng bộ tài khoản lên **Keycloak OIDC SSO** và cấp quyền theo từng Phòng ban / Khoa / Lớp học.

### 6.2. Kiến trúc Bảo mật & Phân quyền 3 Tầng (3-Layer RBAC & Unit ACL)
* **Tầng 1 — Định danh & Vai trò (Keycloak OIDC SSO):** Quản lý 3 vai trò (`SUPER_ADMIN`, `TENANT_ADMIN`, `EMPLOYEE/MEMBER`) gắn liền với `tenant_id` và `department` (Đơn vị trực thuộc).
* **Tầng 2 — Tiền lọc Tri thức Vector (Vector RAG Pre-filtering):** Tài liệu PDF/TXT/MD được trích xuất tự động và vector hóa (3072 chiều với `gemini-embedding-001`), gắn nhãn metadata `tenant_id` và `department_access` để cô lập tri thức ngay từ bước truy vấn.
* **Tầng 3 — Trạm Kiểm soát Con người (LangGraph HITL Interrupt):** Tự động nhận diện ý định tạo đề xuất/đơn từ (`CREATE_REQUEST`), tạm dừng luồng thực thi để người dùng xác nhận và chuyển vào hộp thư phê duyệt của Quản lý.

### 6.3. Động cơ Suy luận LangGraph & Xử lý Ngữ cảnh (AI Context Core)
* Tách biệt luồng xử lý thành các Node chuyên biệt trên đồ thị trạng thái (**LangGraph StateGraph**):
  $$\text{Start Node} \longrightarrow \text{Intent & Thread Router} \longrightarrow \text{Unit ACL Guardrail} \longrightarrow \text{Vector RAG / HITL Engine} \longrightarrow \text{Grounded Response Generator}$$
* Mọi câu trả lời đều đi kèm hộp **Nguồn trích dẫn (Citation Box)** hiển thị rõ tên văn bản gốc, tên tổ chức và điểm tương đồng Cosine.

### 6.4. Giám sát & Kiểm định Định lượng (Langfuse Observability & Eval Pipeline)
* Tích hợp **Trace Log thời gian thực** ngay trên Studio Playground và bảng điều khiển **Langfuse Metrics** giúp Quản trị viên theo dõi độ trễ (P95 Latency), lượng Token tiêu thụ và tỷ lệ trích dẫn chuẩn xác trên từng phiên hội thoại.
