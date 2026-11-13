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

        # ----------------- NODE 1: INTENT & SEARCH -----------------
        state["intent"] = "RAG_SEARCH"

        # ----------------- NODE 2: VECTOR RAG RETRIEVAL & LLM RESPONSE -----------------
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
                f"Người dùng là nhân viên {user_dict['full_name']} (Phòng ban: {user_dict['department']}) của {self.company_name}. "
                f"Người dùng hỏi: '{message}'.\n"
                f"Hãy trả lời với tư cách là {self.agent_name} (chuyên trách phạm vi {self.department_access}) tại {self.company_name}. "
                f"Trả lời chuyên nghiệp, thực tế theo phong cách doanh nghiệp, hỗ trợ tận tình, định dạng HTML dễ đọc (sử dụng <b>, <br>, <ul>, <li>)."
            )
            llm_reply = call_gemini_llm(prompt, self.instruction)
            if llm_reply:
                state["reply"] = llm_reply.replace("\n", "<br>")
            else:
                state["reply"] = f"Dạ em là <b>{self.agent_name}</b> của {self.company_name}. Em sẵn sàng hỗ trợ các vấn đề chuyên môn thuộc phạm vi {self.department_access} cho anh/chị ạ!"
            state["citation"] = f"Trợ lý AI Doanh nghiệp ({self.agent_name}) - {self.company_name}"

        state["latency"] = round(time.time() - start_time, 2)
        state["token_estimate"] = len(message.split()) + len(state["reply"].split()) + 180
        return state
