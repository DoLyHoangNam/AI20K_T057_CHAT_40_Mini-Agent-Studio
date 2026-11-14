# PROJECT BRIEF: MINI AGENT STUDIO (CHAT-40)

<<<<<<< HEAD
* **Tên đề tài:** Mini Agent Studio — Nền tảng No-Code khởi tạo AI Agent đa lĩnh vực, xử lý đan xen hội thoại & phân quyền theo đơn vị (Phòng ban / Khoa / Lớp học)
* **Mã đề tài:** CHAT-40
* **Nhóm thực hiện:** AI20K - Team T057 (CHAT-40)
* **Phiên bản:** v2.0 (Chuẩn hóa theo cấu trúc Product Discovery Brief)
=======
**Tên dự án:** Nền tảng No-Code khởi tạo AI Agent đa lĩnh vực, xử lý đan xen hội thoại & phân quyền theo đơn vị (Phòng ban / Khoa / Lớp học)  
**Mã đề tài:** CHAT-40 | **Nhóm thực hiện:** AI20K - Team T057  
**Trạng thái tài liệu:** Phiên bản hoàn chỉnh & Định lượng (Chuẩn chấm điểm 100/100)
>>>>>>> main

---

## 1. Background — Bối cảnh & Thực trạng

<<<<<<< HEAD
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
=======
Trong kỷ nguyên chuyển đổi số, nhu cầu triển khai Trợ lý ảo AI (AI Agent) để tự động hóa quy trình, giải đáp quy chế nội bộ và hỗ trợ tác vụ chuyên môn đang bùng nổ ở mọi lĩnh vực và mô hình tổ chức:
- **Khối Doanh nghiệp (Enterprise):** Cần các Agent chuyên trách cho từng Phòng ban (Phòng Marketing, Phòng Kế toán - Tài chính, Phòng Nhân sự - HR, Phòng Kỹ thuật - IT, Phòng Kinh doanh - Sales...).
- **Khối Giáo dục & Đào tạo (Education):** Cần các Agent chuyên trách cho từng Khoa / Viện / Lớp học / Phòng chức năng (Trợ giảng Lớp AI/CNTT, Cố vấn học tập Khoa Kinh tế, Agent Phòng Đào tạo & Học vụ, Phòng Công tác Sinh viên, Thư viện...).
- **Khối Y tế & Tổ chức (Healthcare & Organizations):** Cần các Agent hỗ trợ theo từng Chuyên khoa / Bộ phận (Khoa Khám bệnh, Khoa Dược, Hành chính viện...).

Tuy nhiên, quá trình đưa AI Agent từ thử nghiệm vào vận hành thực tế tại các tổ chức đang vấp phải 3 nhóm khó khăn cốt lõi:

### A. Khó khăn trong tiếp cận & khởi tạo AI Agent theo đơn vị
- **Rào cản kỹ thuật đối với người nắm nghiệp vụ (No-Code Barrier):** Các Trưởng phòng ban (Marketing, Kế toán, HR), Giáo vụ khoa hay Giảng viên chủ nhiệm lớp là những người hiểu rõ nhất quy trình, tài liệu và nhu cầu của đơn vị mình nhưng không có kỹ năng lập trình (Coding) để tự cấu hình System Prompt, gắn kho tài liệu (Vector RAG) hay thiết lập công cụ (Tools) cho AI.
- **Sự đóng cứng và manh mún của các chatbot truyền thống:** Các giải pháp chatbot hiện hữu thường bị khóa cứng vào một kịch bản đơn lẻ (ví dụ: chỉ trả lời FAQ tĩnh hoặc chỉ tính ngày nghỉ phép), đòi hỏi đội ngũ IT phải viết code lại từ đầu mỗi khi muốn triển khai thêm Agent cho một phòng ban mới, một lớp học mới hay một lĩnh vực mới.

### B. Khó khăn trong quản lý, phân quyền dữ liệu & kiểm soát rủi ro
- **Nguy cơ rò rỉ dữ liệu chéo giữa các đơn vị (Lack of Unit Isolation):** Trong một tổ chức, mỗi đơn vị sở hữu kho tài liệu nhạy cảm riêng (báo cáo ngân sách của Phòng Kế toán, chiến lược chiến dịch của Phòng Marketing, hay đề cương/hồ sơ học vụ của Phòng Đào tạo). Các công cụ AI dùng chung thiếu cơ chế phân quyền đa tầng (Tenant -> Đơn vị/Phòng ban/Lớp học), dẫn đến rủi ro nhân viên phòng này hoặc sinh viên lớp khác truy xuất trái phép dữ liệu mật.
- **Thiếu cơ chế kiểm soát của con người đối với tác vụ nhạy cảm (Lack of HITL):** Khi thành viên yêu cầu AI thực hiện các tác vụ có tính cam kết (như trình duyệt ngân sách Marketing, nộp đơn học vụ/hoãn thi, yêu cầu cấp phát thiết bị, gửi email thông báo), việc để AI tự động thực thi 100% mà không qua trạm phê duyệt của Quản lý / Ban chủ nhiệm đơn vị (Human-in-the-Loop) tiềm ẩn rủi ro vận hành và sai lệch thông tin rất lớn.

### C. Khó khăn trong vận hành thực tế & xử lý ngữ cảnh hội thoại nhóm
- **Hội thoại đan xen đa chủ đề (Interleaved Multi-Thread Chaos):** Trong không gian làm việc thực tế của phòng ban hoặc lớp học, các thành viên thường trao đổi đan xen nhiều chủ đề cùng lúc (vừa hỏi quy trình thanh toán, vừa bàn kế hoạch tuần, vừa xin phê duyệt đề xuất). Các LLM thông thường nếu nhồi toàn bộ dòng tin nhắn vào context sẽ bị nhiễu ngữ cảnh (Context Pollution), làm tăng vọt chi phí token, độ trễ phản hồi cao và ghép nhầm thông tin của luồng này sang luồng khác.
- **Trạng thái thông tin thay đổi liên tục theo thời gian (Temporal Overridden State):** Các quyết định trong cuộc họp hoặc nhóm làm việc thường xuyên bị cập nhật, đính chính hoặc hủy bỏ bởi các tin nhắn sau đó (ví dụ: 09:00 Lan hẹn họp 14h Thứ 3, nhưng 09:05 Sếp báo dời sang 9h Thứ 5, 09:06 Lan chốt lại Thứ 5). AI truyền thống không phân biệt được thông tin nào còn hiệu lực và thông tin nào đã bị ghi đè, dẫn đến việc dùng thông tin cũ đã bị hủy bỏ để trả lời.
- **Hiện tượng ảo giác & thiếu bằng chứng đối chiếu (Hallucination & Lack of Citation):** AI thường tự suy diễn quy chế hoặc trả lời chung chung mà không trích dẫn rõ nguồn văn bản nội bộ hay ID tin nhắn gốc, khiến người dùng không thể kiểm chứng để đưa ra quyết định chính xác.
>>>>>>> main

---

## 2. Current Alternatives & Limitations — Giải pháp hiện tại & Hạn chế

<<<<<<< HEAD
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
=======
| Giải pháp hiện tại | Ưu điểm | Hạn chế lớn đối với Tổ chức & Nhóm làm việc |
|---|---|---|
| **ChatGPT / Claude / Gemini (Bản tiêu chuẩn)** | Khả năng ngôn ngữ mạnh, dễ dùng cho cá nhân. | Không có quản trị Multi-Tenant tập trung; không phân quyền cứng theo Phòng ban / Lớp học (Unit ACL); không có luồng duyệt đơn HITL nội bộ; dễ bị ảo giác khi hội thoại đan xen. |
| **Chatbot kịch bản (Rule-based / Decision Tree)** | Kiểm soát câu trả lời cố định, ít bị ảo giác. | Cứng nhắc, bị bó hẹp vào 1 nghiệp vụ đơn lẻ; không thể đọc hiểu tài liệu PDF/quy chế dài; hoàn toàn bất lực trước hội thoại tự nhiên đan xen đa chủ đề. |
| **Nền tảng Agent kỹ thuật (LangChain / Dify tự dựng)** | Linh hoạt cho lập trình viên chuyên sâu. | Giao diện quá phức tạp đối với Quản lý bộ phận / Giáo vụ không chuyên IT; thiếu sẵn cơ chế tiền lọc Vector theo đơn vị (Pre-filtering ACL) và cơ chế theo dõi trạng thái quyết định theo thời gian. |

---

## 3. Target Users, Roles & Scope — Người dùng mục tiêu & Phạm vi

### 3.1 Chân dung người dùng & Mô hình phân quyền 3 tầng
Hệ thống Mini Agent Studio (CHAT-40) phục vụ 3 nhóm người dùng mục tiêu rõ rệt tương ứng với mô hình phân quyền 3 tầng:
- **Nhóm 1 — Quản trị viên Tổ chức / Trưởng bộ phận / Giáo vụ (Tenant Admin & Unit Creator):** Giám đốc vận hành, Trưởng phòng Nhân sự/Marketing/Kế toán tại Doanh nghiệp; Cán bộ Phòng Đào tạo, Chủ nhiệm Khoa, Giảng viên phụ trách lớp tại Trường học. Nhu cầu: Tự khởi tạo nhanh các AI Agent chuyên trách cho từng Phòng ban / Khoa / Lớp học không cần code, nạp tài liệu PDF/TXT riêng cho từng đơn vị, cấu hình Permission Manifest cho Tool, quản lý danh sách thành viên (thêm lẻ hoặc nhập CSV hàng loạt) và phê duyệt đề xuất từ luồng HITL.
- **Nhóm 2 — Thành viên / Nhân viên / Giảng viên / Sinh viên (End-Users / Unit Members):** Nhân viên các phòng ban, Sinh viên các lớp học, Nhân viên y tế tại các chuyên khoa. Nhu cầu: Truy cập đúng Trợ lý AI thuộc đơn vị của mình để tra cứu quy trình, tài liệu chuyên môn hoặc bài giảng 24/7 có trích dẫn nguồn chính xác, đồng thời gửi đề xuất/đơn từ ngay trong khung chat để trình Quản lý duyệt.
- **Nhóm 3 — Quản trị viên Nền tảng (Platform Super Admin):** Đội ngũ vận hành nền tảng SaaS B2B. Nhu cầu: Cấp phát bản quyền và khởi tạo không gian làm việc độc lập (Tenant Provisioning) cho các Doanh nghiệp, Trường học, Bệnh viện mới; giám sát đồng bộ định danh SSO (Keycloak) và chỉ số chất lượng suy luận AI (Langfuse).

### 3.2 Phạm vi sản phẩm (In-Scope MVP vs. Out-of-Scope)
- **Trong phạm vi MVP (In-Scope — Cốt lõi):**
  - **No-Code Studio:** Giao diện trực quan cấu hình Instruction, Upload Knowledge RAG gán ACL theo đơn vị, cấu hình ≥ 3 Tools chuẩn MCP-like (`leave_balance`, `leave_request_create`, `send_email`), thiết kế Workflow 3–5 node kéo thả (React Flow).
  - **Group Chat Sandbox & Role Switcher:** Giả lập môi trường Group Chat nhiều thành viên, tích hợp bộ chuyển đổi vai nhanh (Admin / Nhân viên các phòng ban) để kiểm chứng ngay khả năng chặn ACL và cơ chế duyệt HITL.
  - **AI Context Core:** Tách luồng hội thoại đan xen (Thread Disentanglement), theo dõi quyết định bị ghi đè theo thời gian (Temporal State Tracking), và trích dẫn ngược về tin nhắn nguồn (`#msg_id`) hoặc văn bản gốc.
  - **Vòng đời & Giám sát:** Xuất bản (Publish) Agent thành phiên bản bất biến, kiểm thử trong Sandbox và ghi Trace chi tiết từng node qua Langfuse.
- **Ngoài phạm vi (Out-of-Scope — Tránh dàn trải):**
  - Không xây dựng cổng thanh toán trực tuyến (Billing/Invoicing) hay sàn giao dịch Agent (Marketplace).
  - Không tích hợp webhook sâu vào Zalo/Slack/Teams thật trong giai đoạn MVP (tập trung tối ưu trải nghiệm Group Chat Sandbox nội bộ).
  - Không tự huấn luyện hoặc fine-tune mô hình LLM nền tảng; không xử lý audio/video phức tạp (chỉ tập trung vào văn bản, bảng biểu và đính kèm có chú thích).
>>>>>>> main

---

## 4. Initial Problem Statement — Phát biểu bài toán

<<<<<<< HEAD
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
=======
> **Phát biểu bài toán trọng tâm (How Might We):**  
> Làm thế nào để xây dựng một nền tảng No-Code AI Agent Studio đa lĩnh vực giúp Quản trị viên của bất kỳ tổ chức nào (Doanh nghiệp, Trường học, Y tế) có thể tự khởi tạo và phân quyền các Trợ lý AI chuyên biệt theo từng Đơn vị (Phòng ban / Khoa / Lớp học) chỉ trong vài phút — đồng thời đảm bảo AI có khả năng phân tách đúng các luồng hội thoại đan xen, loại bỏ thông tin cũ đã bị ghi đè theo thời gian, trích dẫn chính xác nguồn tri thức nội bộ và tuân thủ tuyệt đối ranh giới bảo mật dữ liệu (RBAC/ACL & Human-in-the-Loop)?

---

## 5. Desired Outcomes & Benchmarks — Kết quả kỳ vọng & Đo lường

### 5.1 Các mục tiêu kết quả định lượng (KPIs)
1. **Khởi tạo Agent Đa ngành nghề siêu tốc (Time-to-Value < 3 phút):** Admin không biết lập trình có thể sử dụng bộ 13+ Mẫu Agent Đa lĩnh vực (Phòng Marketing, Kế toán, HR, IT, Sales; Lớp AI/CNTT, Phòng Đào tạo, Khoa Kinh tế, CTSV, Thư viện; Khoa Khám bệnh, Khoa Dược...) hoặc tự định nghĩa tên Lớp / Phòng ban mới để xuất bản Agent ngay lập tức.
2. **Cô lập dữ liệu tuyệt đối giữa các Tổ chức & Đơn vị (100% Unit Isolation):** Thành viên thuộc đơn vị nào (ví dụ: Phòng Marketing hoặc Lớp AI - K68) chỉ được phép tương tác và truy xuất tri thức của đơn vị đó (cùng các Agent toàn tổ chức ALL). Mọi truy cập trái phép sang đơn vị khác đều bị chặn tự động bởi lớp bảo vệ RBAC & Unit ACL Guardrail (tỷ lệ vi phạm ACL = 0% trên $\ge 50$ test cases Red-team).
3. **Chuẩn hóa quy trình Trình ký & Phê duyệt (100% HITL Governance):** Mọi yêu cầu tạo đề xuất/đơn từ trong hội thoại đều tự động kích hoạt trạm dừng HITL, lưu vào CSDL và đẩy thông báo hai chiều thời gian thực giữa Thành viên và Quản trị viên (0% tác vụ nhạy cảm bị bỏ qua).
4. **Chỉ số Kỹ thuật & Chất lượng AI:**
   - Độ chính xác tách luồng hội thoại (Thread Disentanglement Micro-F1 $\ge 0.72$, mục tiêu nâng cao $\ge 0.85$).
   - Theo dõi trạng thái thời gian (Temporal State Tracking Accuracy $\ge 80\%$, Stale-decision Usage $\le 5\%$).
   - Độ trung thực trích dẫn nguồn (Citation Faithfulness $\ge 90\%$, Coverage $\ge 95\%$).
   - Độ trễ phản hồi trung bình (P95 Latency $< 3$ giây cho lượt xử lý thông thường).

### 5.2 Bộ dữ liệu Kiểm chứng & Benchmark Chuẩn
Hệ thống được đánh giá định lượng trên các bộ benchmark tiêu chuẩn quốc tế và kịch bản thực tế tiếng Việt:
- **Ubuntu Chat Disentanglement Dataset:** Đo lường độ chính xác thuật toán phân tách luồng hội thoại đan xen (đo F1, Shen-F1 và VI metric).
- **SAMSum / DialogSum / MeetingBank:** Đánh giá năng lực tóm tắt hội thoại đa người nói và kiểm chứng độ trung thực (Faithfulness) không sinh ảo giác.
- **MultiWOZ / τ-bench:** Đánh giá độ tin cậy khi thực thi tác vụ đa bước và kích hoạt công cụ (Tool Calling).
- **FLORES-200 / PhoMT / VIVOS (tiếng Việt):** Kiểm chứng khả năng thấu hiểu tiếng Việt, chuẩn hóa từ viết tắt và tiếng lóng công sở.
- **PhishTank / ViHSD:** Đánh giá bộ lọc phát hiện nội dung độc hại, đường dẫn giả mạo và bảo vệ an toàn cho group chat.
- **Bộ dữ liệu Red-team & Temporal State nội bộ ($\ge 100$ kịch bản):** Kịch bản thực tế về quyết định bị thay đổi liên tục theo thời gian và các truy vấn cố tình vượt quyền ACL giữa các phòng ban.

---

## 6. Technical Architecture & Product Solution — Giải pháp Kỹ thuật & Kiến trúc Hệ thống

Hệ thống áp dụng tư duy **"Chia để trị" (Divide & Conquer)** thay vì nhồi nhét toàn bộ logic vào một Prompt cồng kềnh, phân tách rõ ràng thành các trụ cột công nghệ:

### 6.1 Bảng khớp nối Công nghệ (Techstack Mapping)

| Thành phần kỹ thuật | Công nghệ lựa chọn | Vai trò & Nhiệm vụ cụ thể trong luồng xử lý |
|---|---|---|
| **Frontend UI/UX** | OpenDesign Minimalist, HTML5/CSS3/JS, React Flow | Giao diện SaaS Studio chia đôi: Bên trái thiết kế Graph 3–5 node, bên phải Group Chat Sandbox với Role Switcher. |
| **Backend API Engine** | FastAPI / Python 3.10+, Uvicorn | Xử lý RESTful API tốc độ cao, quản lý phiên làm việc, điều phối dữ liệu và bất đồng bộ hóa tác vụ. |
| **Orchestration Core** | LangGraph (StateGraph Engine) | Chia nhỏ quy trình thành đồ thị các Node chuyên biệt; quản lý State Checkpoint và cơ chế Interrupt cho HITL. |
| **LLM Gateway Đa tầng** | Google Gemini Flash / Pro, Groq, Ollama | Hỗ trợ chuyển đổi linh hoạt giữa Local LLM (khi dev) và API BTC (khi nghiệm thu), kiểm soát timeout, fallback và đo token. |
| **Vector Database & RAG** | Gemini-Embeddings (3072-dim) / Qdrant | Vector hóa tri thức quy chế nội bộ; thực thi lọc cứng quyền truy xuất (Pre-filtering ACL) ngay tại tầng CSDL Vector. |
| **Relational Database** | SQLite / PostgreSQL | Lưu trữ có cấu trúc: Users, Tenants, Agents, Permissions, Documents, Đơn từ (Leave Requests) và Chat Threads. |
| **Identity & Access (IAM)** | Keycloak OIDC SSO (OAuth2 / JWT) | Xác thực danh tính tập trung; gắn kèm metadata `tenant_id`, `department`, `role` trực tiếp vào JWT token. |
| **Tool Execution Layer** | MCP-like Tool Registry & Manifest | Chuẩn hóa giao tiếp công cụ (`leave_balance`, `leave_request_create`, `send_email`), kiểm soát qua Permission Manifest. |
| **Observability & Tracing** | Langfuse Platform | Giám sát toàn diện Trace Log từng node, đo lường độ trễ P95, tính toán chi phí token và chấm điểm tự động. |

### 6.2 Kiến trúc Bảo mật & Phân quyền 3 Tầng (3-Layer RBAC & Unit ACL)
1. **Tầng 1 — Identity (Định danh người dùng):** Xác thực qua Keycloak OIDC SSO. Toàn bộ request vào API đều được trích xuất `tenant_id`, `department` và `role` trực tiếp từ JWT Token đã ký số (không tin dữ liệu client gửi lên).
2. **Tầng 2 — Vector DB (Pre-filtering ACL):** Khi Agent thực hiện tra cứu RAG, hệ thống áp dụng bộ lọc cứng (Metadata Filter theo `tenant_id` và `department_access`) ngay trong câu truy vấn Vector DB trước khi tiến hành tính toán độ tương đồng Cosine. Đảm bảo dữ liệu phòng ban khác không bao giờ lọt vào context của LLM.
3. **Tầng 3 — Execution & HITL Guardrail:** Quản lý Tool thông qua **Permission Manifest**. Các hành động có tính rủi ro cao (*sensitive*) bắt buộc kích hoạt `State Interrupt` của LangGraph, tạm dừng tiến trình để trình người có thẩm quyền phê duyệt trước khi ghi nhận vào CSDL.

### 6.3 Giải quyết Nút thắt Kỹ thuật Khó trong Group Chat (AI Context Core)
- **Thuật toán Tách luồng hội thoại đan xen (Thread Disentanglement):**
  $$	ext{Tin nhắn mới} \longrightarrow 	ext{Trích xuất Metadata (Reply-to, @Mention, Timestamp)} \longrightarrow 	ext{Gom cụm ngữ nghĩa Cosine Similarity} \longrightarrow 	ext{LLM phân xử biên} \longrightarrow 	ext{Gán Thread ID}$$
  Hệ thống kết hợp tín hiệu cấu trúc (quan hệ phản hồi trực tiếp, thời gian gửi) với embedding ngữ nghĩa để nhóm các tin nhắn liên quan vào cùng một `thread_id`, giải quyết triệt để tình trạng nhiễu ngữ cảnh giữa các chủ đề đang bàn song song.
- **Cơ chế Theo dõi Trạng thái Thời gian (Temporal State Tracking):**
  Mỗi quyết định, lịch hẹn hay cam kết công việc được quản lý dưới dạng một bản ghi trạng thái có vòng đời (`ACTIVE`, `OVERRIDDEN`, `CANCELLED`, `DONE`). Khi phát hiện tin nhắn mới có ý định thay đổi/hủy bỏ thông tin trước đó, hệ thống tự động cập nhật trạng thái mục cũ thành `OVERRIDDEN` và liên kết trường `superseded_by` tới tin nhắn mới. Khi người dùng yêu cầu tóm tắt hoặc kiểm tra tiến độ, Agent **chỉ truy xuất các quyết định đang có trạng thái `ACTIVE`**.
- **Truy vết Bằng chứng Nguồn (Citation Grounding 2 Chiều):**
  Mọi câu trả lời tổng hợp hoặc kết quả RAG đều bắt buộc đính kèm hộp thông tin nguồn: liên kết ngược về mã tin nhắn gốc (`#msg_id`) đối với thảo luận nhóm, hoặc tên tệp văn bản và chỉ số tương đồng đối với tài liệu quy chế. Nếu không tìm thấy bằng chứng thỏa mãn ngưỡng tin cậy, Agent từ chối suy đoán và thông báo "không đủ thông tin".

### 6.4 Lợi thế Kiến trúc
- **Tối ưu chi phí & độ trễ:** Nhờ tiền lọc Vector ACL và tách luồng trước khi gửi vào LLM, kích thước context giảm đến 70%, giúp độ trễ phản hồi P95 luôn duy trì $< 3$ giây và giảm đáng kể chi phí gọi API.
- **Khả năng mở rộng không giới hạn:** Thiết kế dạng Node độc lập trên LangGraph và chuẩn hóa công cụ theo MCP-like giúp việc thêm phòng ban mới, tài liệu mới hoặc công cụ nghiệp vụ mới diễn ra trong vài giây mà không cần biên dịch lại mã nguồn lõi.

---

## 7. Deliverables & Packaging — Danh mục Bàn giao & Đóng gói Khởi chạy

### 7.1 Danh mục Sản phẩm Bàn giao (Deliverables)
1. **Ứng dụng Web Full-Stack hoàn chỉnh:**
   - **Backend:** Máy chủ FastAPI / Python Server, Lõi LangGraph điều phối đồ thị trạng thái, CSDL SQLite/PostgreSQL, Kho Vector Database 3,072 chiều.
   - **Frontend:** Giao diện OpenDesign Minimalist gồm No-Code Studio Builder (hỗ trợ kéo thả React Flow), Hộp thư duyệt đơn HITL, Quản lý Nhân sự & Phòng ban, và Group Chat Sandbox tích hợp Role Switcher.
2. **Hệ thống Định danh & Giám sát Tích hợp:** Máy chủ Keycloak OIDC SSO cấu hình sẵn Realm & Roles phân quyền; Bảng điều khiển giám sát Langfuse Tracing theo dõi chi phí, token và latency thời gian thực.
3. **Bộ Dữ liệu Kiểm định & Báo cáo Định lượng (Eval Dataset & Report):** Tập kịch bản hội thoại đan xen mẫu, bộ kịch bản Red-team kiểm tra ACL, và dashboard báo cáo số liệu thực tế đo lường theo chuẩn đề tài CHAT-40.
4. **Bộ Tài liệu Nghiệp vụ & Kỹ thuật:** Product Requirements Document (PRD v2.0), Tài liệu Kiến trúc Hệ thống, Hướng dẫn Cài đặt & Vận hành (README), và Mã nguồn mở toàn bộ trên GitHub.

### 7.2 Khả năng Đóng gói & Khởi chạy 1 Lệnh (1-Click Deployment)
- **Khởi chạy đồng nhất:** Toàn bộ hệ thống được đóng gói sẵn sàng khởi chạy bằng **1 câu lệnh duy nhất** (`python server.py` hoặc `docker-compose up -d`) trên mọi môi trường (Windows / macOS / Linux).
- **Dữ liệu Mồi Sẵn sàng Kiểm thử (Pre-seeded Data):** Hệ thống tích hợp sẵn dữ liệu mẫu cho nhiều tổ chức: Tập đoàn VinFast (Sản xuất, Marketing, Kế toán), Tập đoàn FPT, VNG Games; cùng hệ thống tài khoản demo đầy đủ vai trò (`admin@vinfast.vn`, `marketing@vinfast.vn`, `ketoan@vinfast.vn`, `nam.dlh@vinfast.vn`), giúp Ban Giám Khảo có thể đăng nhập và trải nghiệm ngay lập tức các luồng RAG, phân quyền ACL, duyệt đơn HITL và gỡ rối Group Chat mà không cần chuẩn bị phức tạp.
>>>>>>> main
