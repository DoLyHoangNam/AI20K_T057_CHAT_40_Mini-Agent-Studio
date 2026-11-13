# 🎬 KỊCH BẢN THUYẾT TRÌNH & DEMO DAY (5 PHÚT VÀNG)
> **Dự án:** CHAT-40 — Mini Agent Studio  
> **Người trình bày:** Leader / Đại diện nhóm T057  
> **Mục tiêu:** Thể hiện trọn vẹn 3 năng lực cốt lõi: **RAG Đọc Tài Liệu Thật**, **Bảo Mật Phân Quyền ACL**, và **Human-In-The-Loop (HITL) Kết Nối Database**.

---

### ⏱️ PHÚT 0:00 – 1:00 | MỞ ĐẦU & NÊU BÀI TOÁN
- **Lời thoại mở đầu:**
  > *"Kính thưa Hội đồng và quý thầy cô, trong doanh nghiệp lớn như VinFast với hàng chục phòng ban khác nhau, nhân viên thường xuyên bị quá tải vì không biết hỏi ai về quy chế, tra cứu ngày phép rất thủ công và quy trình ký duyệt đơn từ mất nhiều ngày. Nhóm T057 chúng em xây dựng giải pháp **Mini Agent Studio** — nền tảng No-Code cho phép doanh nghiệp cấu hình và xuất bản các AI Agent thông minh có tích hợp sẵn RAG, CSDL thật và cơ chế an toàn Human-In-The-Loop."*

---

### ⏱️ PHÚT 1:00 – 2:30 | DEMO CỔNG NHÂN VIÊN (RAG & ACL)
*(Thao tác trên màn hình: Mở trình duyệt vào `http://localhost:8000/login.html`)*

1. **Thao tác 1 (Đăng nhập nhân viên):**
   - Bấm vào thẻ **Đỗ Lý Hoàng Nam (Sản xuất)**.
   - **Lời thoại:** *"Đầu tiên, em đăng nhập với vai trò anh Nam thuộc phòng Sản xuất xưởng. Ở cột bên trái, hệ thống lập tức tải số liệu chấm công thực tế từ SQLite: thâm niên 8 tháng, tiêu chuẩn 8 ngày phép và số ngày còn lại."*

2. **Thao tác 2 (Kiểm tra Phân quyền ACL):**
   - Click vào *Trợ lý Kế toán & Hóa đơn* bị khóa màu đỏ ở cột trái.
   - **Lời thoại:** *"Tại đây, hệ thống áp dụng cơ chế ACL Security: Do anh Nam thuộc phòng Sản xuất, Bot Kế toán chứa tài liệu mật bị khóa chặt và không cho phép truy cập."*

3. **Thao tác 3 (Test RAG Tìm kiếm Ngữ nghĩa trên Vector DB):**
   - Bấm nút câu hỏi nhanh: *"Logo VinFast được phép đặt trên nền màu gì?"*
   - **Lời thoại:** *"Em đặt câu hỏi về quy chuẩn thương hiệu. Câu hỏi này được chuyển thành vector 3072 chiều qua Gemini-Embedding-001, tính khoảng cách Cosine trên Vector DB thật và trích xuất đúng Điều 1 trong văn bản nội bộ kèm Score tương đồng 0.87."*

---

### ⏱️ PHÚT 2:30 – 4:00 | DEMO QUY TRÌNH HUMAN-IN-THE-LOOP (HITL)
*(Đây là phần "ăn điểm" cao nhất của đồ án)*

1. **Thao tác 1 (Kích hoạt luồng xin nghỉ phép):**
   - Nhập: *"Tôi muốn xin nghỉ 1 ngày"* ➔ Nhập tiếp: *"Thứ 6 ngày mai đi việc gia đình"*.
   - **Lời thoại:** *"Khi người dùng muốn xin nghỉ, Agent không vội vàng thực thi ngay mà kích hoạt cơ chế an toàn **Human-In-The-Loop**. Trạng thái hội thoại bị ngắt (Interrupt), hiển thị bảng xác nhận chi tiết để người dùng kiểm tra thông tin."*

2. **Thao tác 2 (Xác nhận gửi đơn):**
   - Bấm nút **"Xác nhận gửi đơn"**.
   - **Lời thoại:** *"Sau khi người dùng xác nhận, đơn được lưu ngay vào bảng `leave_requests` trong SQLite và chuyển lên hòm thư Quản trị viên."*

3. **Thao tác 3 (Admin Duyệt đơn Real-time):**
   - Mở tab mới: `http://localhost:8000/admin_studio.html` ➔ Bấm tab **"Duyệt Đơn Nghỉ"**.
   - Thấy đơn `#1` đang ở trạng thái `PENDING` ➔ Bấm nút **"Duyệt đơn"**.
   - **Lời thoại:** *"Phía Quản lý, Admin kiểm tra và bấm Duyệt. Cơ sở dữ liệu SQLite ngay lập tức cập nhật trạng thái đơn thành APPROVED và tự động cộng dồn số ngày đã nghỉ của nhân viên."*

4. **Thao tác 4 (Nhân viên nhận thông báo tức thì):**
   - Quay lại tab nhân viên: Chỉ vào **Popup Banner thông báo màu xanh** vừa nhảy lên và thanh chỉ số phép năm tự động nhảy số mới.
   - **Lời thoại:** *"Phía nhân viên, không cần tải lại trang, hệ thống lập tức hiển thị thông báo thời gian thực và cập nhật số ngày phép còn lại ngay lập tức!"*

---

### ⏱️ PHÚT 4:00 – 5:00 | TRÌNH DIỄN DATABASE & KẾT LUẬN
*(Mở tab `http://localhost:8000/database_viewer.html`)*

- **Lời thoại kết luận:**
  > *"Để chứng minh toàn bộ dữ liệu là thực tế 100%, em mở trang Database Explorer kết nối trực tiếp với file SQLite `database.db`. Các bảng `users`, `leave_requests`, `agents` đều được đồng bộ nhất quán. Hệ thống đáp ứng trọn vẹn 5 tiêu chí nghiệm thu của đề tài CHAT-40. Em xin cảm ơn Hội đồng và sẵn sàng nhận câu hỏi phản biện ạ!"*
