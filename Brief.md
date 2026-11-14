# PROJECT BRIEF: MINI AGENT STUDIO (CHAT-40)

* **Tên dự án:** Nền tảng No-Code tạo AI Agent đa lĩnh vực, xử lý đan xen hội thoại & phân quyền theo đơn vị (Mini Agent Studio)
* **Mã đề tài:** CHAT-40
* **Đơn vị phát triển:** AI20K - Team CHAT-40

---

## 1. Bối Cảnh & Vấn Đề (The Problem)

Nhu cầu triển khai AI Agent để tự động hóa quy trình, tra cứu tri thức nội bộ và hỗ trợ cộng tác nhóm đang bùng nổ ở **mọi ngành nghề** — từ **Doanh nghiệp** (chia theo các phòng ban: Marketing, Kế toán, Nhân sự, IT, Sales...), **Giáo dục / Trường học** (chia theo Khoa, Viện, Lớp học, Phòng Đào tạo...), đến **Y tế, Tổ chức & Cộng đồng**. Tuy nhiên, việc đưa AI Agent vào vận hành thực tế đang vấp phải hai rào cản lớn:

1. **Rào cản Kỹ thuật & Tính đóng cứng (Technical & Domain Barrier):**
   * Các Quản lý bộ phận (Trưởng phòng Marketing/Kế toán, Giáo vụ, Chủ nhiệm lớp, Admin tổ chức) nắm rõ quy trình chuyên môn nhưng **không có kỹ năng lập trình (Coding)** để tự cấu hình công cụ (Tools), nạp kho tri thức (RAG) và thiết lập luồng nghiệp vụ (Workflow) riêng cho từng đơn vị.
   * Các giải pháp chatbot truyền thống thường bị bó hẹp vào một kịch bản cố định (như chỉ hỏi đáp FAQ hoặc chỉ làm một tác vụ đơn lẻ), không thể linh hoạt mở rộng cho nhiều phòng ban hay nhiều lĩnh vực khác nhau.
2. **Sự hỗn loạn của Môi trường Thực tế (Context Chaos trong Group Chat):**
   * Khác với chat 1-1 tuyến tính, khi đưa AI Agent vào không gian làm việc chung hoặc Group Chat của phòng ban / lớp học, AI thường bị tê liệt hoặc sinh ra ảo giác (*Hallucination*) do:
     * **Hàng loạt chủ đề đan xen cùng lúc (Interleaved Threads):** Nhiều thành viên trao đổi song song các chủ đề khác nhau.
     * **Ngôn ngữ đặc thù theo ngành:** Thuật ngữ chuyên ngành (Marketing, Kế toán, Học vụ, Kỹ thuật), từ viết tắt, tiếng lóng nội bộ.
     * **Quyết định bị ghi đè liên tục theo thời gian thực (Temporal Overridden State):** Tin nhắn sau phủ định hoặc cập nhật lại quyết định của tin nhắn trước.
     * **Rủi ro rò rỉ dữ liệu chéo & thực thi lệnh nhầm:** Thiếu cơ chế cô lập dữ liệu giữa các đơn vị (ví dụ: nhân viên Marketing truy cập nhầm tài liệu mật của phòng Kế toán, hoặc sinh viên lớp này sửa dữ liệu lớp khác) và thiếu vòng lặp phê duyệt của con người (*Human-in-the-Loop - HITL*).

---

## 2. Giải Pháp Đề Xuất (The Solution)

**Mini Agent Studio** là nền tảng SaaS Multi-Tenant & Multi-Domain gồm 2 cấu phần cốt lõi:
* **Giao diện No-Code Builder đa lĩnh vực (Dành cho Creator/Admin):** Thiết kế trực quan luồng Agent Graph, khởi tạo nhanh các Agent chuyên trách theo từng **Đơn vị / Phòng ban / Lớp học / Chuyên khoa** chỉ với vài thao tác.
* **AI Context Core (Động cơ xử lý ngôn ngữ & phân quyền):** Giải quyết triệt để sự hỗn loạn ngữ cảnh trong hội thoại và kiểm soát phân quyền đa tầng theo đơn vị.

### 2.1. Năng Lực Kỹ Thuật Cốt Lõi (Core Capabilities)
* **Tách luồng hội thoại đan xen (Thread Disentanglement):** Kết hợp thuật toán gom cụm ngữ nghĩa với LLM để phân lập các luồng chủ đề độc lập trong cùng một dòng tin nhắn liên tục.
* **Theo dõi Trạng thái Thời gian (Temporal State Tracking):** Tự động phát hiện và đánh dấu các *"Quyết định đã bị thay đổi/hủy bỏ"* (Overridden State), ngăn chặn việc Agent sử dụng thông tin cũ đã bị sửa đổi.
* **Kiểm soát Phân quyền 3 Tầng đa ngành nghề (3-Layer RBAC & Unit ACL):**
  * **Tầng 1 - Identity:** 3 vai trò chuẩn (`SUPER_ADMIN` / `TENANT_ADMIN` / `EMPLOYEE` — đại diện cho Thành viên / Nhân sự / Sinh viên của tổ chức) kèm thuộc tính `tenant_id`, `department` (Đơn vị: Phòng ban / Khoa / Lớp học), `is_approver`, xác thực qua Keycloak OIDC SSO.
  * **Tầng 2 - Vector DB (Metadata Filter theo Đơn vị):** Lọc cứng theo `tenant_id` + `department` (Đơn vị/Lớp/Phòng ban) ngay tại tầng truy vấn vector **trước** khi xếp hạng; đảm bảo Agent và người dùng của đơn vị nào chỉ truy xuất được tri thức của đơn vị đó (hoặc tri thức chung `ALL` của tổ chức).
  * **Tầng 3 - LangGraph Execution & HITL:** Quản lý Tool qua Permission Manifest; tự động tạm dừng luồng và gửi yêu cầu phê duyệt cho cấp quản lý (Human-in-the-Loop) đối với các tác vụ nhạy cảm (phê duyệt đề xuất/đơn từ, gửi thông báo diện rộng, cập nhật dữ liệu).

### 2.2. Trải Nghiệm Người Dùng (Split-Screen Architecture)
* **Khu vực Studio (Nửa trái):** Trực quan hóa quy trình 3–5 node. Creator chọn mẫu lĩnh vực (Doanh nghiệp: Marketing, Kế toán, HR, IT, Sales; Giáo dục: Lớp học, Khoa/Viện, Phòng Đào tạo; Y tế: Chuyên khoa; hoặc Tự định nghĩa đơn vị), cấu hình prompt, tải tài liệu RAG theo đơn vị và bật/tắt Tool.
* **Khu vực Sandbox (Nửa phải):** Giả lập hội thoại thực tế với **Role & Unit Switcher** linh hoạt (chuyển đổi tức thì giữa Admin / Thành viên Đơn vị A như Phòng Marketing hoặc Lớp AI-01 / Thành viên Đơn vị B như Phòng Kế toán hoặc Lớp KT-02) để kiểm thử ngay ranh giới phân quyền ACL, cách Agent phản ứng và cơ chế HITL.

---

## 3. Lợi Thế Cạnh Tranh & Kiến Trúc (Technical Highlights)

Hệ thống áp dụng tư duy **"Chia để trị" (Divide & Conquer)** thay vì nhồi nhét vào một Prompt cồng kềnh:

* **Thích ứng Đa Ngành Nghề (Domain-Agnostic Unit Isolation):** Cùng một lõi kiến trúc nhưng tự động đáp ứng mô hình Doanh nghiệp (theo Phòng ban), Trường học (theo Khoa/Lớp), Bệnh viện (theo Chuyên khoa) mà không bị khóa cứng vào một nghiệp vụ đơn lẻ.
* **LLM Gateway Đa Tầng:** Hỗ trợ linh hoạt chuyển đổi giữa Local LLM (Ollama/Groq) trong quá trình dev và API của BTC / Gemini khi nghiệm thu mà không cần sửa code lõi.
* **Graph-based Workflow (LangGraph):** Chia nhỏ luồng suy luận thành các Node chuyên biệt:  
  $$\text{Node Tách luồng} \longrightarrow \text{Node Kiểm tra quyền (ACL)} \longrightarrow \text{Node RAG / Tool} \longrightarrow \text{Node Trả lời}$$
* **Truy vết Bằng chứng (Citation Grounding):** Mọi tóm tắt, trích dẫn hay câu trả lời của Agent bắt buộc phải gắn kèm ID tin nhắn nguồn hoặc tên văn bản gốc của đơn vị.
* **Kiểm định Định lượng (Evaluation Pipeline):** Tích hợp Langfuse để đo lường tự động độ chính xác phân luồng, độ trung thực (Faithfulness) dựa trên các bộ benchmark tiêu chuẩn: *Ubuntu Chat Disentanglement, SAMSum, MultiWOZ*.

---

## 4. Mục Tiêu Đầu Ra (Deliverables)

1. **Sản phẩm Web hoàn chỉnh:**
   * **Backend:** FastAPI / Python Server, LangGraph Core, Vector DB (Qdrant / JSON Index có lọc ACL theo đơn vị), Keycloak OIDC SSO.
   * **Frontend:** OpenDesign Minimalist, Split-Screen Studio Builder (hỗ trợ đa lĩnh vực & phân quyền theo đơn vị/phòng ban/lớp học) & Chat Portal/Sandbox.
2. **Dữ liệu đánh giá (Eval Dataset):** Bộ kịch bản hội thoại đan xen thực tế đa lĩnh vực, tích hợp dashboard theo dõi điểm số định lượng trên Langfuse.
3. **Bộ tài liệu bàn giao:** Product Requirements Document (PRD), Wireframe UI/UX, Báo cáo kỹ thuật định lượng và mã nguồn hoàn chỉnh trên GitHub.

> **Cam kết:** Mini Agent Studio không dừng lại ở một chatbot đơn nhiệm, mà là nền tảng khởi tạo AI Agent đa lĩnh vực — chứng minh bằng số liệu định lượng khả năng hiểu đúng ngữ cảnh hội thoại và cô lập quyền truy cập dữ liệu tuyệt đối giữa các phòng ban, lớp học và tổ chức.
