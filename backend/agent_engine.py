import os
import json
import urllib.request
import time
from typing import Dict, Any, List
from vector_store import vector_search

API_KEY = os.environ.get("GEMINI_API_KEY", "")

def call_gemini_llm(prompt: str, system_instruction: str = "") -> str:
    """Gọi Google Gemini Flash LLM sinh phản hồi tự nhiên, chuẩn xác 100%"""
    if not API_KEY:
        return "Lỗi: Không tìm thấy GEMINI_API_KEY."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
    
    contents = []
    if system_instruction:
        contents.append({
            "role": "user",
            "parts": [{"text": f"[CHỈ DẪN HỆ THỐNG]: {system_instruction}\n\n[YÊU CẦU]: {prompt}"}]
        })
    else:
        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 800
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Lỗi gọi Gemini LLM: {e}")
        return ""

class LangGraphAgent:
    """
    State Graph Engine mô phỏng kiến trúc LangGraph chuẩn đồ án:
    State: { user, message, intent, context, interrupt_hitl, reply, latency, token_estimate }
    Hỗ trợ Multi-Tenant Isolation: Phân lập tri thức & thương hiệu tuyệt đối giữa các Doanh nghiệp!
    """
    def __init__(self, agent_name: str, instruction: str, department_access: str, tenant_id: str = "VINFAST"):
        self.agent_name = agent_name
        self.instruction = instruction
        self.department_access = department_access
        self.tenant_id = tenant_id

        # Tên hiển thị của doanh nghiệp
        tenant_brand_map = {
            "VINFAST": "Tập đoàn VinFast",
            "FPT": "Tập đoàn FPT",
            "VNG": "VNG Games",
            "PLATFORM": "Hệ thống Nền tảng"
        }
        self.company_name = tenant_brand_map.get(tenant_id, tenant_id)

    def run(self, user_dict: Dict[str, Any], message: str) -> Dict[str, Any]:
        start_time = time.time()
        state: Dict[str, Any] = {
            "user": user_dict,
            "message": message,
            "intent": "UNKNOWN",
            "rag_context": "",
            "citation": "",
            "interrupt_hitl": False,
            "reply": "",
            "latency": 0.0,
            "token_estimate": 0
        }

        # ----------------- NODE 1: INTENT CLASSIFICATION -----------------
        msg_lower = message.lower()
        if any(k in msg_lower for k in ["định mức", "hạn mức", "chỉ số", "còn lại", "hồ sơ", "tác vụ", "nhiệm vụ", "tiêu chuẩn", "ngân sách", "bao nhiêu ngày", "mấy ngày", "quỹ phép", "phép năm", "ngày nghỉ"]):
            state["intent"] = "QUOTA_INQUIRY"
        elif any(k in msg_lower for k in ["đề xuất", "yêu cầu", "làm đơn", "nộp đơn", "trình ký", "phê duyệt", "tạo phiếu", "xin nghỉ", "nghỉ phép"]):
            state["intent"] = "CREATE_REQUEST"
        else:
            state["intent"] = "RAG_SEARCH"

        # ----------------- NODE 2: ENTERPRISE OPERATIONAL QUOTA TOOL NODE -----------------
        if state["intent"] == "QUOTA_INQUIRY":
            attrs = {}
            raw_attrs = user_dict.get("attributes")
            if raw_attrs:
                try:
                    attrs = json.loads(raw_attrs) if isinstance(raw_attrs, str) else raw_attrs
                except Exception:
                    attrs = {}
            assigned = attrs.get("assigned_quota", user_dict.get("total_leave_days", 20) or 20)
            processed = attrs.get("processed_quota", user_dict.get("used_leave_days", 5) or 5)
            available = attrs.get("available_quota", assigned - processed)

            prompt = (
                f"Người dùng {user_dict['full_name']} (Phòng ban: {user_dict['department']}) của đơn vị {self.company_name} hỏi: '{message}'.\n"
                f"Dữ liệu hồ sơ vận hành thực tế trong SQLite: Thâm niên {user_dict.get('tenure_months', 12)} tháng, "
                f"Định mức tác vụ/đề xuất tiêu chuẩn: {assigned} lượt, Đã hoàn thành/xử lý: {processed} lượt, "
                f"Khả dụng hiện tại: {available} lượt.\n"
                f"Hãy đóng vai {self.agent_name} của {self.company_name}, trả lời lịch sự, chuyên nghiệp theo phong cách doanh nghiệp, "
                f"làm nổi bật các chỉ số định mức và số lượt khả dụng (in đậm bằng HTML)."
            )
            llm_text = call_gemini_llm(prompt, self.instruction)
            if llm_text:
                state["reply"] = llm_text.replace("\n", "<br>")
            else:
                state["reply"] = (
                    f"Dạ theo <b>Hồ sơ công tác & Nhiệm vụ</b> của anh/chị <b>{user_dict['full_name']}</b> tại {self.company_name}:<br>"
                    f"• Phòng ban: <b>{user_dict['department']}</b> (Thâm niên: {user_dict.get('tenure_months', 12)} tháng)<br>"
                    f"• Định mức tác vụ / đề xuất: <b>{assigned} lượt</b><br>"
                    f"• Đã xử lý / hoàn thành: <b class='text-warning'>{processed} lượt</b><br>"
                    f"👉 Hiện tại anh/chị <b>CÒN LẠI: <span class='text-success fs-5 fw-bold'>{available} lượt khả dụng</span></b> để tạo đề xuất hoặc phân công tác vụ mới ạ!"
                )
            state["citation"] = f"Cơ sở dữ liệu SQLite: Bảng `users` & Quy chế Vận hành {self.company_name}."

        # ----------------- NODE 3: HITL INTERRUPT NODE -----------------
        elif state["intent"] == "CREATE_REQUEST":
            state["interrupt_hitl"] = True
            state["reply"] = f"Dạ em đã ghi nhận nhu cầu tạo đề xuất / yêu cầu nghiệp vụ của anh/chị tại {self.company_name}. Em đang chuẩn bị biểu mẫu và kích hoạt cơ chế bảo mật Human-In-The-Loop để trình ký Quản lý."
            state["citation"] = f"Quy trình Human-In-The-Loop (HITL) - Quy chế Vận hành {self.company_name}"

        # ----------------- NODE 4: VECTOR RAG RETRIEVAL & LLM RESPONSE -----------------
        else:
            search_results = vector_search(message, tenant_id=self.tenant_id, department_access=self.department_access, top_k=2)
            if search_results and search_results[0]["score"] > 0.35:
                top_match = search_results[0]
                context_texts = [f"[{r['source']} - Độ tương đồng: {r['score']:.2f}]:\n{r['text']}" for r in search_results]
                state["rag_context"] = "\n\n---\n\n".join(context_texts)
                sources = list(set([r['source'] for r in search_results]))
                state["citation"] = f"Vector Database (Gemini-Embed-001): `{sources[0]}` [{self.company_name}] (Cosine: {top_match['score']:.2f})"

                prompt = (
                    f"Dưới đây là các đoạn trích xuất từ Vector Database quy định chính thức của {self.company_name} ({self.tenant_id}):\n\n"
                    f"{state['rag_context']}\n\n"
                    f"Người dùng hỏi: '{message}'.\n"
                    f"Dựa chính xác vào ngữ cảnh trên để trả lời ngắn gọn, đầy đủ ý, định dạng HTML dễ đọc (dùng <br>, <b>, <ul>, <li>). "
                    f"Tuyệt đối không trích dẫn quy định của công ty khác."
                )
                llm_reply = call_gemini_llm(prompt, self.instruction)
                if llm_reply:
                    state["reply"] = llm_reply.replace("\n", "<br>")
                else:
                    state["reply"] = f"Dạ theo văn bản quy chuẩn <b>{top_match['source']}</b> của {self.company_name}:<br><br>{top_match['text'].replace(chr(10), '<br>')}"
            else:
                prompt = (
                    f"Người dùng hỏi: '{message}'. "
                    f"Hãy trả lời ngắn gọn và lịch sự, nêu rõ bạn là {self.agent_name} của {self.company_name} và gợi ý người dùng hỏi về: "
                    f"1. Tra cứu định mức tác vụ và chỉ số nghiệp vụ cá nhân, 2. Tạo đề xuất trình ký nghiệp vụ (HITL), 3. Nội quy quy chế và hướng dẫn vận hành tại {self.company_name}."
                )
                llm_reply = call_gemini_llm(prompt, self.instruction)
                if llm_reply:
                    state["reply"] = llm_reply.replace("\n", "<br>")
                else:
                    state["reply"] = f"Dạ em là <b>{self.agent_name}</b> của {self.company_name}. Em có thể hỗ trợ tra cứu quy chế, kiểm tra định mức tác vụ hoặc hỗ trợ lập đề xuất nghiệp vụ trình ký Quản lý ạ!"
                state["citation"] = f"Cổng Trợ lý ảo Doanh nghiệp {self.company_name}"

        state["latency"] = round(time.time() - start_time, 2)
        state["token_estimate"] = len(message.split()) + len(state["reply"].split()) + 180
        return state
