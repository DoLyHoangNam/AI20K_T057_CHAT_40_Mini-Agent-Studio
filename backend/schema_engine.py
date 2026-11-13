import json
import re
import ast
from typing import Dict, Any, Optional
from agent_engine import call_gemini_llm

PRESET_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "ENTERPRISE": {
        "domain_type": "ENTERPRISE",
        "profile_card": {
            "title": "Hồ sơ công tác & Nhiệm vụ",
            "scope_label": "Phòng ban",
            "metrics": [
                {"key": "assigned_quota", "label": "Định mức tác vụ", "unit": "lượt"},
                {"key": "processed_quota", "label": "Đã hoàn thành", "unit": "lượt"},
                {"key": "available_quota", "label": "Khả dụng", "unit": "lượt", "formula": "assigned_quota - processed_quota"}
            ]
        },
        "actions": [
            {
                "intent": "CREATE_REQUEST",
                "label": "Tạo đề xuất & Yêu cầu nghiệp vụ",
                "approver_role": "TENANT_ADMIN",
                "fields": ["Nội dung đề xuất", "Căn cứ / Lý do", "Thời hạn hoàn thành"],
                "guard": "available_quota > 0"
            }
        ],
        "terms": {
            "user": "Nhân sự",
            "request": "Đề xuất nghiệp vụ",
            "admin": "Quản lý / Trưởng bộ phận"
        }
    },
    "EDUCATION": {
        "domain_type": "EDUCATION",
        "profile_card": {
            "title": "Hồ sơ học vụ sinh viên",
            "scope_label": "Khoa / Viện",
            "metrics": [
                {"key": "credits_total", "label": "Chương trình", "unit": "tín chỉ"},
                {"key": "credits_done", "label": "Đã tích lũy", "unit": "tín chỉ"},
                {"key": "credits_left", "label": "Còn lại", "unit": "tín chỉ", "formula": "credits_total - credits_done"}
            ]
        },
        "actions": [
            {
                "intent": "CREATE_REQUEST",
                "label": "Nộp đơn hoãn thi / rút môn",
                "approver_role": "TENANT_ADMIN",
                "fields": ["Môn học", "Lý do", "Học kỳ"],
                "guard": "credits_left > 0"
            }
        ],
        "terms": {
            "user": "Sinh viên",
            "request": "Đơn học vụ",
            "admin": "Phòng Đào tạo"
        }
    },
    "HEALTHCARE": {
        "domain_type": "HEALTHCARE",
        "profile_card": {
            "title": "Hồ sơ y tế & Điều trị",
            "scope_label": "Chuyên khoa",
            "metrics": [
                {"key": "coverage_limit", "label": "Hạn mức BHYT", "unit": "%"},
                {"key": "used_coverage", "label": "Đã sử dụng", "unit": "%"},
                {"key": "remain_coverage", "label": "Còn lại", "unit": "%", "formula": "coverage_limit - used_coverage"}
            ]
        },
        "actions": [
            {
                "intent": "CREATE_REQUEST",
                "label": "Đăng ký xét nghiệm / hội chẩn",
                "approver_role": "TENANT_ADMIN",
                "fields": ["Chuyên khoa", "Triệu chứng", "Bác sĩ phụ trách"],
                "guard": "remain_coverage > 0"
            }
        ],
        "terms": {
            "user": "Bệnh nhân",
            "request": "Hồ sơ yêu cầu khám",
            "admin": "Bác sĩ trưởng khoa"
        }
    }
}

def safe_eval_formula(formula: str, values: Dict[str, Any]) -> float:
    """Đánh giá an toàn biểu thức toán học + - * / () không dùng eval() tùy tiện."""
    if not formula or not isinstance(formula, str):
        return 0.0
    
    # Chỉ cho phép biến chữ, số, dấu cách và toán tử
    clean_formula = formula.strip()
    if not re.match(r'^[a-zA-Z0-9_+\-/*().\s]+$', clean_formula):
        return 0.0
        
    tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|[0-9]+(?:\.[0-9]+)?|[+\-/*()]', clean_formula)
    expr_parts = []
    for tok in tokens:
        if tok in '+-/*()':
            expr_parts.append(tok)
        elif re.match(r'^[0-9]+(?:\.[0-9]+)?$', tok):
            expr_parts.append(tok)
        else:
            val = values.get(tok, 0)
            try:
                val_num = float(val) if val is not None else 0.0
            except (ValueError, TypeError):
                val_num = 0.0
            expr_parts.append(str(val_num))
            
    expr_str = " ".join(expr_parts)
    try:
        parsed = ast.parse(expr_str, mode='eval')
        for node in ast.walk(parsed):
            if not isinstance(node, (
                ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
                ast.Add, ast.Sub, ast.Mult, ast.Div, ast.USub, ast.UAdd
            )):
                return 0.0
        
        compiled = compile(parsed, '<formula>', 'eval')
        result = eval(compiled, {"__builtins__": {}}, {})
        if isinstance(result, (int, float)):
            if result == int(result):
                return int(result)
            return round(result, 2)
        return 0.0
    except Exception:
        return 0.0

def sanitize_text(text: Any) -> str:
    """Xóa bỏ các thẻ html nguy hiểm như <script>."""
    if not isinstance(text, str):
        return str(text or "")
    # Xóa script tags
    cleaned = re.sub(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', text, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r'<\s*script[^>]*>', '', cleaned, flags=re.IGNORECASE)
    return cleaned.strip()

def validate_schema(schema: Any) -> Optional[Dict[str, Any]]:
    """Kiểm tra cấu trúc và tính hợp lệ của UI Schema."""
    if not isinstance(schema, dict):
        return None
        
    domain_type = sanitize_text(schema.get("domain_type", "CUSTOM")).upper() or "CUSTOM"
    profile_card = schema.get("profile_card")
    if not isinstance(profile_card, dict):
        return None
        
    title = sanitize_text(profile_card.get("title", "Hồ sơ nghiệp vụ"))
    scope_label = sanitize_text(profile_card.get("scope_label", "Phòng ban"))
    raw_metrics = profile_card.get("metrics", [])
    if not isinstance(raw_metrics, list) or len(raw_metrics) == 0:
        return None
        
    clean_metrics = []
    for m in raw_metrics:
        if isinstance(m, dict) and "key" in m and "label" in m:
            clean_metrics.append({
                "key": sanitize_text(m.get("key")),
                "label": sanitize_text(m.get("label")),
                "unit": sanitize_text(m.get("unit", "")),
                "formula": sanitize_text(m.get("formula", ""))
            })
            
    if len(clean_metrics) == 0:
        return None

    raw_actions = schema.get("actions", [])
    clean_actions = []
    if isinstance(raw_actions, list):
        for act in raw_actions:
            if isinstance(act, dict) and "label" in act:
                clean_actions.append({
                    "intent": sanitize_text(act.get("intent", "CREATE_REQUEST")),
                    "label": sanitize_text(act.get("label", "Tạo yêu cầu")),
                    "approver_role": sanitize_text(act.get("approver_role", "TENANT_ADMIN")),
                    "fields": [sanitize_text(f) for f in act.get("fields", []) if f],
                    "guard": sanitize_text(act.get("guard", ""))
                })
                
    if not clean_actions:
        clean_actions = [
            {
                "intent": "CREATE_REQUEST",
                "label": "Tạo yêu cầu phê duyệt",
                "approver_role": "TENANT_ADMIN",
                "fields": ["Nội dung yêu cầu", "Lý do"],
                "guard": ""
            }
        ]

    terms = schema.get("terms", {})
    if not isinstance(terms, dict):
        terms = {}
    clean_terms = {
        "user": sanitize_text(terms.get("user", "Người dùng")),
        "request": sanitize_text(terms.get("request", "Yêu cầu")),
        "admin": sanitize_text(terms.get("admin", "Quản trị viên"))
    }

    return {
        "domain_type": domain_type,
        "profile_card": {
            "title": title,
            "scope_label": scope_label,
            "metrics": clean_metrics
        },
        "actions": clean_actions,
        "terms": clean_terms
    }

def get_tenant_schema_preset(domain_type: str = "ENTERPRISE") -> Dict[str, Any]:
    """Lấy preset schema tương ứng theo domain_type."""
    dt = (domain_type or "ENTERPRISE").upper().strip()
    return PRESET_SCHEMAS.get(dt, PRESET_SCHEMAS["ENTERPRISE"])

def generate_schema_from_llm(description: str, sample_text: str = "", domain_type: str = "CUSTOM") -> Dict[str, Any]:
    """Sử dụng Google Gemini LLM để sinh UI Profile Schema tự động theo mô tả nghiệp vụ."""
    system_instruction = (
        "Bạn là Chuyên gia Kiến trúc Hệ thống UI Schema (Schema-Driven UI Architect).\n"
        "Nhiệm vụ của bạn là đọc mô tả lĩnh vực hoặc tài liệu của tổ chức (Doanh nghiệp, Trường học, Bệnh viện, v.v.), "
        "tự tư duy và sinh ra một bản UI Profile Schema chuẩn JSON để giao diện người dùng tự thích ứng.\n"
        "Bắt buộc trả về ĐÚNG ĐỊNH DẠNG JSON hợp lệ duy nhất, không kèm giải thích bên ngoài.\n"
        "Cấu trúc JSON yêu cầu:\n"
        "{\n"
        '  "domain_type": "TÊN_LĨNH_VỰC",\n'
        '  "profile_card": {\n'
        '    "title": "Tiêu đề thẻ hồ sơ (ví dụ: Hồ sơ học vụ sinh viên)",\n'
        '    "scope_label": "Tên nhãn phân nhóm (ví dụ: Khoa / Viện hoặc Chuyên khoa)",\n'
        '    "metrics": [\n'
        '      {"key": "tên_thuộc_tính_1", "label": "Tên hiển thị 1", "unit": "đơn_vị"},\n'
        '      {"key": "tên_thuộc_tính_2", "label": "Tên hiển thị 2", "unit": "đơn_vị"},\n'
        '      {"key": "tên_thuộc_tính_3", "label": "Tên hiển thị 3", "unit": "đơn_vị", "formula": "tên_thuộc_tính_1 - tên_thuộc_tính_2"}\n'
        '    ]\n'
        '  },\n'
        '  "actions": [\n'
        '    {\n'
        '      "intent": "CREATE_REQUEST",\n'
        '      "label": "Tên nút nộp yêu cầu",\n'
        '      "approver_role": "TENANT_ADMIN",\n'
        '      "fields": ["Trường 1", "Trường 2"],\n'
        '      "guard": "tên_thuộc_tính_3 > 0"\n'
        '    }\n'
        '  ],\n'
        '  "terms": {\n'
        '    "user": "Danh xưng người dùng (Sinh viên/Bệnh nhân/Nhân viên)",\n'
        '    "request": "Tên loại đơn từ",\n'
        '    "admin": "Danh xưng cấp quản lý duyệt"\n'
        '  }\n'
        "}"
    )

    prompt = f"Lĩnh vực/Mô tả tổ chức: {description}\nTài liệu tham khảo mẫu: {sample_text[:1000]}"
    try:
        raw_output = call_gemini_llm(prompt, system_instruction)
        if raw_output:
            # Loại bỏ markdown code blocks ```json ... ```
            clean_str = re.sub(r'^```json\s*', '', raw_output.strip(), flags=re.IGNORECASE)
            clean_str = re.sub(r'```$', '', clean_str.strip())
            parsed_json = json.loads(clean_str)
            validated = validate_schema(parsed_json)
            if validated:
                return validated
    except Exception as e:
        print(f"Lỗi khi AI sinh schema: {e}")

    # Fallback an toàn về preset
    fallback = get_tenant_schema_preset(domain_type)
    return fallback

def resolve_user_attributes(user_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Phân giải thuộc tính của người dùng: kết hợp attributes JSON và các cột legacy."""
    attrs = {}
    raw_attrs = user_dict.get("attributes")
    if raw_attrs and isinstance(raw_attrs, str):
        try:
            parsed = json.loads(raw_attrs)
            if isinstance(parsed, dict):
                attrs.update(parsed)
        except Exception:
            pass
    elif isinstance(raw_attrs, dict):
        attrs.update(raw_attrs)

    # Đảm bảo các thuộc tính doanh nghiệp & legacy được nạp vào
    total_val = user_dict.get("total_leave_days", 20) or 20
    used_val = user_dict.get("used_leave_days", 5) or 5
    if "assigned_quota" not in attrs:
        attrs["assigned_quota"] = total_val
    if "processed_quota" not in attrs:
        attrs["processed_quota"] = used_val
    if "total_leave_days" not in attrs:
        attrs["total_leave_days"] = total_val
    if "used_leave_days" not in attrs:
        attrs["used_leave_days"] = used_val
    if "tenure_months" not in attrs:
        attrs["tenure_months"] = user_dict.get("tenure_months", 12)

    return attrs
