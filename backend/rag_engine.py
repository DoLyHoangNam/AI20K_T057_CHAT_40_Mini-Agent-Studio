import os
import re

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def search_knowledge(agent_name: str, query: str):
    """
    RAG Search engine: Quét toàn văn các văn bản tài liệu thực tế của VinFast trong thư mục data/
    và trích xuất đúng đoạn liên quan kèm trích dẫn văn bản chuẩn xác.
    """
    query_lower = query.lower()
    
    # Xác định file tài liệu phù hợp theo Agent hoặc câu hỏi
    target_files = []
    if "marketing" in agent_name.lower() or "marketing" in query_lower:
        target_files.append("Noi_quy_Phong_Marketing_VinFast.txt")
    elif "kế toán" in agent_name.lower() or "ke toan" in agent_name.lower() or any(w in query_lower for w in ["hóa đơn", "công tác phí", "thanh toán"]):
        target_files.append("Quy_che_Tai_chinh_Ke_toan.txt")
    else:
        target_files.append("Quy_che_Nhan_su_VinFast_2026.txt")
        target_files.append("Noi_quy_Phong_Marketing_VinFast.txt")

    best_match = None
    best_score = 0
    matched_doc = ""

    keywords = [w for w in re.split(r'\s+', query_lower) if len(w) > 2 and w not in ["như", "thế", "nào", "được", "không", "cho", "tôi", "hỏi", "là", "gì"]]

    for fname in target_files:
        fpath = os.path.join(DATA_DIR, fname)
        if not os.path.exists(fpath):
            continue
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue

        paragraphs = content.split("\n\n")
        for p in paragraphs:
            p_clean = p.strip()
            if not p_clean:
                continue
            score = sum(1 for kw in keywords if kw in p_clean.lower())
            if score > best_score:
                best_score = score
                best_match = p_clean
                matched_doc = fname

    if best_match and best_score >= 1:
        # Định dạng đoạn trích dẫn đẹp mắt
        formatted_text = best_match.replace("\n", "<br>")
        return {
            "found": True,
            "text": formatted_text,
            "source": matched_doc
        }

    return {"found": False, "text": "", "source": ""}
