 PROJECT BRIEF: MINI AGENT STUDIO (CHAT-40)

* **Tên dự án:** Nền tảng No-Code tạo AI Agent xử lý đan xen hội thoại & phân quyền (Mini Agent Studio)
* **Mã đề tài:** CHAT-40
* **Đơn vị phát triển:** AI20K - Team CHAT-40

---

## 1. Bối Cảnh & Vấn Đề (The Problem)

Trong môi trường doanh nghiệp hiện đại, việc sử dụng AI Agent để tự động hóa quy trình, tra cứu tài liệu và hỗ trợ công việc đang trở thành xu hướng tất yếu. Tuy nhiên, việc đưa AI Agent vào thực tế đang vấp phải hai rào cản lớn:

1. **Rào cản Kỹ thuật (Technical Barrier):**
   * Các Quản lý dự án (PM), HR Manager, Admin cộng đồng có nghiệp vụ chuyên môn sâu nhưng **không có kỹ năng lập trình (Coding)** để tự cấu hình công cụ (Tools), tích hợp RAG và xây dựng luồng nghiệp vụ (Workflow).
2. **Sự hỗn loạn của Môi trường Thực tế (Context Chaos trong Group Chat):**
   * Khác với chat 1-1 tuyến tính, khi đưa AI Agent vào Group Chat doanh nghiệp, AI thường bị tê liệt hoặc sinh ra ảo giác (*Hallucination*) do:
     * **Hàng loạt chủ đề đan xen cùng lúc (Interleaved Threads):** Nhiều thành viên hỏi và thảo luận các vấn đề khác nhau song song.
     * **Ngôn ngữ nội bộ:** Tiếng lóng, viết tắt, thuật ngữ công sở.
     * **Quyết định bị ghi đè liên tục theo thời gian thực (Temporal Overridden State):** Tin nhắn sau phủ định hoặc thay đổi quyết định của tin nhắn trước.
     * **Rủi ro rò rỉ dữ liệu mật & thực thi lệnh nhầm:** Thiếu cơ chế phân quyền dữ liệu và thiếu vòng lặp phê duyệt của con người (*Human-in-the-Loop - HITL*).

---

## 2. Giải Pháp Đề Xuất (The Solution)

**Mini Agent Studio** là hệ sinh thái khép kín gồm 2 cấu phần cốt lõi:
* **Giao diện No-Code Builder (Dành cho Creator):** Thiết kế trực quan, kéo thả trực tiếp luồng Agent Graph.
* **AI Context Core (Động cơ xử lý ngôn ngữ trong Group Chat):** Giải quyết triệt để sự hỗn loạn ngữ cảnh và kiểm soát phân quyền đa tầng.

### 2.1. Năng Lực Kỹ Thuật Cốt Lõi (Core Capabilities)
* **Tách luồng hội thoại đan xen (Thread Disentanglement):** Kết hợp thuật toán gom cụm ngữ nghĩa với LLM để phân lập các luồng hội thoại độc lập trong cùng một dòng tin nhắn liên tục.
* **Theo dõi Trạng thái Thời gian (Temporal State Tracking):** Tự động phát hiện và đánh dấu các *"Quyết định đã bị thay đổi/hủy bỏ"* (Overridden State), ngăn chặn việc Agent sử dụng thông tin cũ đã bị sửa đổi.
* **Kiểm soát Phân quyền 3 Tầng (3-Layer RBAC & ACL):**
* **Tầng 1 - Identity:** Phân quyền vai trò người dùng (Admin, Member, Intern) xác thực qua Keycloak OIDC SSO.
  * **Tầng 2 - Vector DB (Qdrant Metadata Filter):** Lọc cứng quyền truy xuất tại kho vector; đảm bảo LLM không bao giờ truy vấn ra dữ liệu vượt quyền hạn.
  * **Tầng 3 - LangGraph Execution & HITL:** Quản lý Tool qua Permission Manifest; tự động tạm dừng luồng và gửi yêu cầu phê duyệt cho con người (Human-in-the-Loop) đối với các lệnh nhạy cảm (duyệt phép, gửi mail, xóa dữ liệu).

### 2.2. Trải Nghiệm Người Dùng (Split-Screen Architecture)
* **Khu vực Studio (Nửa trái):** Trực quan hóa quy trình bằng React Flow. Creator cấu hình prompt, tải tài liệu RAG, chọn phòng ban, kết nối Tool (Google Calendar, Jira, Email).
* **Khu vực Sandbox (Nửa phải):** Giả lập Group Chat thực tế với **Role Switcher** linh hoạt (chuyển đổi tức thì giữa Admin, Nhân viên, Thực tập sinh) để kiểm thử ngay cách Agent phản ứng và cơ chế HITL.

---

## 3. Lợi Thế Cạnh Tranh & Kiến Trúc (Technical Highlights)

Hệ thống áp dụng tư duy **"Chia để trị" (Divide & Conquer)** thay vì nhồi nhét vào một Prompt cồng kềnh:

* **LLM Gateway Đa Tầng:** Hỗ trợ linh hoạt chuyển đổi giữa Local LLM (Ollama/Groq) trong quá trình dev và API của BTC khi nghiệm thu mà không cần sửa code lõi.
* **Graph-based Workflow (LangGraph):** Chia nhỏ luồng suy luận thành các Node chuyên biệt:  
  $$\text{Node Tách luồng} \longrightarrow \text{Node Kiểm tra quyền} \longrightarrow \text{Node RAG / Tool} \longrightarrow \text{Node Trả lời}$$
* **Truy vết Bằng chứng (Citation Grounding):** Mọi tóm tắt, trích dẫn hay câu trả lời của Agent bắt buộc phải gắn kèm ID tin nhắn nguồn hoặc tên văn bản gốc.
* **Kiểm định Định lượng (Evaluation Pipeline):** Tích hợp Langfuse để đo lường tự động độ chính xác phân luồng, độ trung thực (Faithfulness) dựa trên các bộ benchmark tiêu chuẩn: *Ubuntu Chat Disentanglement, SAMSum, MultiWOZ*.

---

## 4. Mục Tiêu Đầu Ra (Deliverables)

1. **Sản phẩm Web hoàn chỉnh:**
   * **Backend:** FastAPI / Python Server, LangGraph Core, Qdrant Vector DB, Keycloak OIDC SSO.
   * **Frontend:** OpenDesign Minimalist, Split-Screen Studio Builder & Group Chat Sandbox.
2. **Dữ liệu đánh giá (Eval Dataset):** Bộ kịch bản hội thoại đan xen thực tế, tích hợp dashboard theo dõi điểm số định lượng trên Langfuse.
3. **Bộ tài liệu bàn giao:** Product Requirements Document (PRD), Wireframe UI/UX, Báo cáo kỹ thuật định lượng và mã nguồn hoàn chỉnh trên GitHub.
> **Cam kết:** Mini Agent Studio không dừng lại ở mức giao diện demo, mà chứng minh bằng số liệu định lượng khả năng "sống sót", hiểu đúng ngữ cảnh và bảo mật dữ liệu tuyệt đối trong môi trường làm việc thực tế.
