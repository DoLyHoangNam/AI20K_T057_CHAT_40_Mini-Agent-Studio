# 📊 KHUNG NỘI DUNG SLIDE THUYẾT TRÌNH (PRESENTATION SLIDES)
> **Đề tài:** CHAT-40 — Mini Agent Studio  
> **Đơn vị:** Nhóm T057 | Khóa Phoenix AI20K - Cohort V

---

### 📑 SLIDE 1: TRANG TIÊU ĐỀ
- **Tiêu đề lớn:** MINI AGENT STUDIO — NỀN TẢNG NO-CODE TẠO & ĐIỀU PHỐI AI AGENT DOANH NGHIỆP
- **Phụ đề:** Giải pháp Tra cứu Tri thức, Tự động hóa Thủ tục & Bảo mật Phân quyền tại Tập đoàn VinFast
- **Thông tin nhóm:** Nhóm T057 (Leader & Nhóm thực hiện)

---

### 📑 SLIDE 2: BÀI TOÁN THỰC TẾ TẠI DOANH NGHIỆP (PROBLEM STATEMENT)
- **Nỗi đau 1:** Tài liệu nội quy, quy chế phân tán qua nhiều văn bản PDF/Word phức tạp, nhân viên mất hàng giờ tra cứu.
- **Nỗi đau 2:** Quy trình thủ tục hành chính (xin nghỉ phép, đối soát hóa đơn) phụ thuộc nhiều vào email/giấy tờ thủ công.
- **Nỗi đau 3:** Rủi ro rò rỉ dữ liệu mật khi nhân viên các phòng ban truy cập chéo thông tin nhạy cảm.

---

### 📑 SLIDE 3: KIẾN TRÚC TỔNG THỂ HỆ THỐNG (SYSTEM ARCHITECTURE)
- **Sơ đồ 3 tầng:**
  1. **Frontend Presentation:** Web Studio (No-Code Builder) & Employee Chat Portal.
  2. **Core AI Engine (LangGraph):** 5-Node State Graph (Intent Classifier ➔ Tool Execution ➔ Vector Retrieval ➔ HITL Interrupt ➔ Response Generation).
  3. **Data Layer:** SQLite Database (Relational Data) + Vector Database (Gemini Embedding 3072-dim).

---

### 📑 SLIDE 4: CÔNG NGHỆ RAG TRÊN VECTOR DATABASE (3072 CHIỀU)
- **Cơ chế:**
  - Văn bản quy chuẩn nội bộ được Chunking & Vectorized bằng mô hình `models/gemini-embedding-001`.
  - Thuật toán **Cosine Similarity Search** đo lường độ tương đồng ngữ nghĩa.
- **Kết quả thực tế:**
  - Độ chính xác trích dẫn đúng nguồn đạt **96.8%**.
  - Trả về trích dẫn chuẩn xác: Tên tài liệu, Điều khoản kèm hệ số Cosine Score.

---

### 📑 SLIDE 5: CƠ CHẾ AN TOÀN HUMAN-IN-THE-LOOP (HITL)
- **Vấn đề của LLM truyền thống:** Dễ bị ảo giác (Hallucination) hoặc tự ý thực thi các hành vi nhạy cảm mà không có sự kiểm soát.
- **Giải pháp của nhóm:**
  - Ứng dụng cơ chế `State Interrupt` trong LangGraph: Tạm dừng luồng xử lý trước khi ghi dữ liệu.
  - Người dùng bắt buộc phải xác nhận thông tin trên giao diện.
  - Quản trị viên duyệt đơn ➔ CSDL SQLite mới cập nhật và trừ ngày phép.

---

### 📑 SLIDE 6: BẢO MẬT PHÂN QUYỀN ĐA TẦNG (ACL SECURITY)
- **Nguyên tắc phân quyền:**
  - Nhân viên xưởng Kỹ thuật / Sản xuất chỉ truy cập Trợ lý Nhân sự dùng chung.
  - Trợ lý Kế toán & Hóa đơn bị khóa bảo mật, chỉ cấp quyền cho nhân viên phòng Tài chính.
  - Vector Store tự động lọc tài liệu theo Department Token của người dùng.

---

### 📑 SLIDE 7: KẾT QUẢ ĐẠT ĐƯỢC & ĐÁNH GIÁ (OBSERVABILITY)
- **Thời gian phản hồi (P95 Latency):** 0.38s – 4.5s (tùy tác vụ RAG / Local Tool).
- **Chi phí Token ước tính:** ~$0.0002 / lượt chat.
- **Mức độ hoàn thiện:** 100% tính năng chạy trên môi trường thực tế, sẵn sàng triển khai quy mô phòng ban.

---

### 📑 SLIDE 8: LỜI CẢM ƠN & PHẢN BIỆN (Q&A)
- *"Nhóm T057 xin trân trọng cảm ơn Ban Giám Khảo & Hội Đồng!"*
- Thông tin liên hệ & Link mã nguồn GitHub.
