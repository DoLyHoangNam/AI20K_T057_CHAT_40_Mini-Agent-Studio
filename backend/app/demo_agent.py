"""
Prototype Agent: Demonstrating Agent capabilities (Reasoning, RAG Knowledge, Tools, Human-in-the-Loop)
Designed for AI20K - CHAT-40 Mini Agent Studio
"""
import os
import json

# 1. KNOWLEDGE (RAG Mẫu) - Tra cứu tài liệu nội bộ
def tool_tra_cuu_noi_quy(tu_khoa: str) -> str:
    """Tra cứu nội quy VinFast 2026 từ file tài liệu mẫu"""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "Noi_quy_VinFast_sample.txt"))
    if not os.path.exists(file_path):
        return "Không tìm thấy file tài liệu nội quy."
    
    with open(file_path, "r", encoding="utf-8") as f:
        noi_dung = f.read()
    
    # Tìm đoạn văn bản liên quan
    lines = [line for line in noi_dung.split("\n") if tu_khoa.lower() in line.lower() or len(tu_khoa) < 3]
    return "\n".join(lines[:6]) if lines else "Không có điều khoản phù hợp trong tài liệu."

# 2. TOOL 1: Tính toán nghiệp vụ
def tool_tinh_ngay_phep(so_thang_lam_viec: int, so_nam_tham_nien: int = 0) -> int:
    """Tính số ngày phép năm dựa trên thâm niên và thời gian làm việc"""
    if so_thang_lam_viec < 12:
        return so_thang_lam_viec
    base = 12
    bonus = max(0, so_nam_tham_nien - 4) # Từ năm thứ 5 cộng thêm 1 ngày/năm
    return min(20, base + bonus)

# 3. TOOL 2: Tạo đơn xin nghỉ phép (Nhạy cảm - cần Human-in-the-loop)
def tool_tao_don_xin_nghi(ten_nhan_vien: str, so_ngay: int, ly_do: str, da_xac_nhan_hitl: bool = False) -> str:
    """Hành động gửi đơn xin nghỉ lên hệ thống. Yêu cầu xác nhận con người (HITL)."""
    if not da_xac_nhan_hitl:
        return "[YÊU_CẦU_XÁC_NHẬN_HITL]: Bạn có chắc chắn muốn nộp đơn nghỉ phép này lên Quản lý không?"
    
    return f"[THÀNH CÔNG] Đã tạo đơn nghỉ phép cho {ten_nhan_vien} ({so_ngay} ngày, lý do: {ly_do}) và gửi tới Quản lý phê duyệt."

# 4. AGENT RUNNER MÔ PHỎNG (Logic Agent điều phối luồng)
def run_agent_workflow(user_query: str, hitl_confirmed: bool = False):
    print("=" * 60)
    print(f"🤖 [NGƯỜI DÙNG HỎI]: \"{user_query}\"")
    print("=" * 60)
    
    # BƯỚC 1: Lập luận (Reasoning)
    print("🧠 [AGENT SUY NGHĨ]: Phân tích câu hỏi...")
    
    if "mấy ngày phép" in user_query.lower() or "tính phép" in user_query.lower():
        # Trích xuất số tháng (giả lập 8 tháng)
        so_thang = 8
        print(f"⚙️ [AGENT GỌI TOOL]: Gọi tool_tinh_ngay_phep(so_thang={so_thang})...")
        so_phep = tool_tinh_ngay_phep(so_thang)
        print(f"📥 [KẾT QUẢ TOOL]: {so_phep} ngày phép.")
        
        print("📚 [AGENT GỌI RAG]: Tra cứu trích dẫn điều khoản quy định...")
        trich_dan = tool_tra_cuu_noi_quy("tháng")
        
        print("\n💬 [AGENT TRẢ LỜI]:")
        print(f"Chào bạn, bạn làm việc được {so_thang} tháng thì được hưởng {so_phep} ngày phép năm.")
        print(f"📌 [Nguồn trích dẫn]:\n{trich_dan.strip()}\n")
        
    elif "xin nghỉ" in user_query.lower():
        print("⚙️ [AGENT GỌI TOOL]: Soạn thảo đơn xin nghỉ phép...")
        result = tool_tao_don_xin_nghi("Đỗ Lý Hoàng Nam", 3, "Khám bệnh", da_xac_nhan_hitl=hitl_confirmed)
        
        if "[YÊU_CẦU_XÁC_NHẬN_HITL]" in result:
            print("🛡️ [HUMAN-IN-THE-LOOP KÍCH HOẠT]:")
            print("⚠️ CẢNH BÁO: Đây là thao tác tạo dữ liệu chính thức vào hệ thống nhân sự.")
            print(f"👉 Trạng thái: DỪNG LẠI CHỜ PHÊ DUYỆT (Interrupt)")
            print("🔘 [Giao diện hiện nút]: [1. ĐỒNG Ý NỘP]  |  [2. HỦY BỎ]")
        else:
            print("\n💬 [AGENT TRẢ LỜI]:")
            print(result)

if __name__ == "__main__":
    # Test case 1: Hỏi đáp tri thức kết hợp tính toán
    run_agent_workflow("Em làm việc được 8 tháng thì được nghỉ mấy ngày phép?")
    
    # Test case 2: Hành động tạo đơn cần con người xác nhận (HITL)
    run_agent_workflow("Tôi muốn xin nghỉ 3 ngày để đi khám bệnh")
    
    # Test case 3: Sau khi con người bấm "Đồng ý"
    print("\n>>> [NGƯỜI DÙNG BẤM NÚT 'ĐỒNG Ý NỘP'] <<<")
    run_agent_workflow("Tôi muốn xin nghỉ 3 ngày để đi khám bệnh", hitl_confirmed=True)
