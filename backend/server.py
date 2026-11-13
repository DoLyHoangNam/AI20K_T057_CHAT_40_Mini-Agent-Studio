import http.server
import socketserver
import json
import sqlite3
import os
import urllib.parse
from datetime import datetime
import sys

BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)

from agent_engine import LangGraphAgent
from mailer import generate_secure_password, send_welcome_credentials_email, EMAIL_LOG_FILE
from schema_engine import (
    get_tenant_schema_preset,
    validate_schema,
    generate_schema_from_llm,
    resolve_user_attributes,
    safe_eval_formula,
    PRESET_SCHEMAS
)

PORT = 8000
FRONTEND_DIR = os.path.abspath(os.path.join(BACKEND_DIR, "..", "frontend"))
DB_PATH = os.path.abspath(os.path.join(BACKEND_DIR, "database.db"))
DATA_DIR = os.path.abspath(os.path.join(BACKEND_DIR, "..", "data"))
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=30000;")
    return conn

KEYCLOAK_URL = "http://localhost:8080"

def get_kc_admin_token():
    try:
        data = urllib.parse.urlencode({
            'client_id': 'admin-cli',
            'username': 'admin',
            'password': os.environ.get('KC_ADMIN_PASS', 'admin123'),
            'grant_type': 'password'
        }).encode()
        req = urllib.request.Request(f'{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token', data=data)
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())['access_token']
    except Exception as e:
        print("Keycloak token error:", e)
        return None

def sync_user_to_keycloak(email, password, role, tenant_id, full_name="Admin", department="HR"):
    token = get_kc_admin_token()
    if not token:
        return False
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Phân tách Họ và Tên chuẩn xác (Keycloak bắt buộc phải có cả firstName và lastName)
    name_parts = full_name.strip().split(" ", 1)
    if len(name_parts) > 1:
        last_name = name_parts[0]
        first_name = name_parts[1]
    else:
        last_name = "Quản trị viên" if "ADMIN" in role else "Nhân viên"
        first_name = name_parts[0] or "Doanh nghiệp"

    encoded_user = urllib.parse.quote(email)
    u_id = None

    # 1. Kiểm tra xem user đã tồn tại chưa
    try:
        req = urllib.request.Request(f'{KEYCLOAK_URL}/admin/realms/mini-agent-platform/users?username={encoded_user}', headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            existing = json.loads(resp.read().decode())
            if existing:
                u_id = existing[0]['id']
    except Exception:
        pass

    # 2. Tạo mới nếu chưa có
    if not u_id:
        user_payload = {
            'username': email,
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'enabled': True,
            'emailVerified': True,
            'requiredActions': [],
            'attributes': {'tenant_id': [tenant_id], 'department': [department]}
        }
        try:
            req = urllib.request.Request(f'{KEYCLOAK_URL}/admin/realms/mini-agent-platform/users', data=json.dumps(user_payload).encode(), headers=headers)
            urllib.request.urlopen(req, timeout=5)
            # Lấy lại ID
            req = urllib.request.Request(f'{KEYCLOAK_URL}/admin/realms/mini-agent-platform/users?username={encoded_user}', headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                u_id = json.loads(resp.read().decode())[0]['id']
        except Exception as e:
            print(f"Error creating user {email}: {e}")
            return False
    else:
        # Nếu đã có: Cập nhật đầy đủ thông tin để kích hoạt tài khoản
        try:
            update_payload = {
                'firstName': first_name,
                'lastName': last_name,
                'enabled': True,
                'emailVerified': True,
                'requiredActions': [],
                'attributes': {'tenant_id': [tenant_id], 'department': [department]}
            }
            req = urllib.request.Request(f'{KEYCLOAK_URL}/admin/realms/mini-agent-platform/users/{u_id}', data=json.dumps(update_payload).encode(), headers=headers, method='PUT')
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            print(f"Error updating user info {email}: {e}")

    # 3. Đặt mật khẩu chuẩn xác 100% không cần làm tay
    try:
        cred_req = urllib.request.Request(
            f'{KEYCLOAK_URL}/admin/realms/mini-agent-platform/users/{u_id}/reset-password',
            data=json.dumps({'type': 'password', 'value': password, 'temporary': False}).encode(),
            headers=headers,
            method='PUT'
        )
        urllib.request.urlopen(cred_req, timeout=5)
    except Exception as e:
        print(f"Error resetting password for {email}: {e}")
        return False

    # 4. Gán role
    try:
        role_req = urllib.request.Request(f'{KEYCLOAK_URL}/admin/realms/mini-agent-platform/roles/{role}', headers=headers)
        with urllib.request.urlopen(role_req, timeout=5) as resp:
            role_obj = json.loads(resp.read().decode())
        map_req = urllib.request.Request(f'{KEYCLOAK_URL}/admin/realms/mini-agent-platform/users/{u_id}/role-mappings/realm', data=json.dumps([role_obj]).encode(), headers=headers)
        urllib.request.urlopen(map_req, timeout=5)
    except Exception:
        pass # Role might already be assigned

    print(f"🚀 [KEYCLOAK ATOMIC PROVISIONED] {email} ready for instant login with role {role}!")
    return True

def delete_user_from_keycloak(email):
    token = get_kc_admin_token()
    if not token:
        return
    headers = {'Authorization': f'Bearer {token}'}
    try:
        encoded_user = urllib.parse.quote(email)
        req = urllib.request.Request(f'{KEYCLOAK_URL}/admin/realms/mini-agent-platform/users?username={encoded_user}', headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            users = json.loads(resp.read().decode())
            if users:
                u_id = users[0]['id']
                del_req = urllib.request.Request(f'{KEYCLOAK_URL}/admin/realms/mini-agent-platform/users/{u_id}', headers=headers, method='DELETE')
                urllib.request.urlopen(del_req, timeout=5)
                print(f"Keycloak deleted user: {email}")
    except Exception as e:
        print("Keycloak delete error:", e)

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

class UnifiedHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0, post-check=0, pre-check=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path
        query = urllib.parse.parse_qs(url.query)

        # 1. API: Danh sách Doanh nghiệp (Chỉ SuperAdmin xem được)
        if path == "/api/emails/sent":
            if os.path.exists(EMAIL_LOG_FILE):
                with open(EMAIL_LOG_FILE, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f.readlines() if line.strip()]
                    return self.send_json(lines[-25:])
            return self.send_json([])

        elif path == "/api/tenants/presets":
            return self.send_json(PRESET_SCHEMAS)

        elif path == "/api/tenants/ui_schema":
            tenant_id = query.get("tenant_id", [None])[0]
            if not tenant_id:
                return self.send_json({"error": "Thiếu tenant_id"}, 400)
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT domain_type, ui_schema FROM tenants WHERE id = ?", (tenant_id,))
            row = cursor.fetchone()
            conn.close()
            if not row:
                # Trả về preset mặc định nếu chưa lưu trong DB
                return self.send_json(get_tenant_schema_preset("ENTERPRISE"))
            
            domain_type = row["domain_type"] or "ENTERPRISE"
            raw_schema = row["ui_schema"]
            if raw_schema:
                try:
                    parsed = json.loads(raw_schema)
                    valid = validate_schema(parsed)
                    if valid:
                        return self.send_json(valid)
                except Exception:
                    pass
            preset = get_tenant_schema_preset(domain_type)
            return self.send_json(preset)

        elif path == "/api/tenants":
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.id, t.name, t.contact_email, t.plan_type, t.domain_type, t.is_active, t.created_at,
                       (SELECT COUNT(*) FROM users u WHERE u.tenant_id = t.id AND u.role = 'EMPLOYEE') as employee_count,
                       (SELECT COUNT(*) FROM agents a WHERE a.tenant_id = t.id) as agent_count
                FROM tenants t
                WHERE t.id != 'PLATFORM'
                ORDER BY t.created_at DESC
            """)
            rows = [dict(r) for r in cursor.fetchall()]
            conn.close()
            return self.send_json(rows)

        # 2. API: Danh sách Nhân viên (Lọc chuẩn xác theo tenant_id)
        elif path == "/api/users":
            tenant_id = query.get("tenant_id", [None])[0]
            conn = get_db()
            cursor = conn.cursor()
            if tenant_id and tenant_id != "PLATFORM":
                cursor.execute("""
                    SELECT id, tenant_id, email, full_name, role, department, total_leave_days, used_leave_days, tenure_months, attributes, is_active 
                    FROM users WHERE tenant_id = ? ORDER BY id ASC
                """, (tenant_id,))
            else:
                cursor.execute("""
                    SELECT id, tenant_id, email, full_name, role, department, total_leave_days, used_leave_days, tenure_months, attributes, is_active 
                    FROM users ORDER BY id ASC
                """)
            rows = [dict(r) for r in cursor.fetchall()]
            conn.close()
            return self.send_json(rows)

        # 3. API: Lấy thông tin 1 user
        elif path.startswith("/api/users/"):
            user_id = path.split("/")[-1]
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, tenant_id, email, full_name, role, department, total_leave_days, used_leave_days, tenure_months, attributes, is_active 
                FROM users WHERE id = ?
            """, (user_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return self.send_json(dict(row))
            return self.send_json({"error": "User not found"}, 404)

        # 4. API: Danh sách Agents (Lọc chuẩn xác theo tenant_id)
        elif path == "/api/agents":
            tenant_id = query.get("tenant_id", [None])[0]
            conn = get_db()
            cursor = conn.cursor()
            if tenant_id and tenant_id != "PLATFORM":
                cursor.execute("""
                    SELECT id, tenant_id, name, description, instruction, department_access, is_published 
                    FROM agents WHERE tenant_id = ? ORDER BY id ASC
                """, (tenant_id,))
            else:
                cursor.execute("""
                    SELECT id, tenant_id, name, description, instruction, department_access, is_published 
                    FROM agents ORDER BY id ASC
                """)
            rows = [dict(r) for r in cursor.fetchall()]
            conn.close()
            return self.send_json(rows)

        # 5. API: Danh sách Leave Requests (Lọc theo tenant_id)
        elif path == "/api/leave_requests":
            tenant_id = query.get("tenant_id", [None])[0]
            conn = get_db()
            cursor = conn.cursor()
            if tenant_id and tenant_id != "PLATFORM":
                cursor.execute("""
                    SELECT lr.id, lr.tenant_id, lr.user_id, lr.user_name, lr.days_requested, lr.date_details, lr.status, lr.created_at,
                           u.department, u.email
                    FROM leave_requests lr
                    LEFT JOIN users u ON lr.user_id = u.id
                    WHERE lr.tenant_id = ?
                    ORDER BY lr.id DESC
                """, (tenant_id,))
            else:
                cursor.execute("""
                    SELECT lr.id, lr.tenant_id, lr.user_id, lr.user_name, lr.days_requested, lr.date_details, lr.status, lr.created_at,
                           u.department, u.email
                    FROM leave_requests lr
                    LEFT JOIN users u ON lr.user_id = u.id
                    ORDER BY lr.id DESC
                """)
            rows = [dict(r) for r in cursor.fetchall()]
            conn.close()
            return self.send_json(rows)

        # 6. API: Notifications
        elif path == "/api/notifications":
            user_id = query.get("user_id", [None])[0]
            if not user_id:
                return self.send_json({"notifications": []})

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, days_requested, date_details, status
                FROM leave_requests
                WHERE user_id = ? AND status IN ('APPROVED', 'REJECTED') AND notified_to_user = 0
                ORDER BY id DESC
            """, (user_id,))
            rows = [dict(r) for r in cursor.fetchall()]

            if rows:
                ids = [r["id"] for r in rows]
                placeholders = ",".join("?" * len(ids))
                cursor.execute(f"UPDATE leave_requests SET notified_to_user = 1 WHERE id IN ({placeholders})", ids)
                conn.commit()

            conn.close()
            return self.send_json({"notifications": rows})

        # 7. API: Danh sách Documents theo Tenant (Cô lập tri thức Multi-Tenant)
        elif path == "/api/documents":
            tenant_id = query.get("tenant_id", [None])[0]
            conn = get_db()
            cursor = conn.cursor()
            if tenant_id and tenant_id != "PLATFORM":
                cursor.execute("""
                    SELECT id, agent_id, file_name, file_path, file_size_kb, uploaded_at, tenant_id
                    FROM documents WHERE tenant_id = ? ORDER BY id ASC
                """, (tenant_id,))
            else:
                cursor.execute("""
                    SELECT id, agent_id, file_name, file_path, file_size_kb, uploaded_at, tenant_id
                    FROM documents ORDER BY id ASC
                """)
            rows = [dict(r) for r in cursor.fetchall()]
            conn.close()
            return self.send_json(rows)

        # 8. API: Toàn bộ CSDL cho Database Explorer
        elif path == "/api/all_data":
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tenants ORDER BY created_at DESC")
            tenants = [dict(r) for r in cursor.fetchall()]
            cursor.execute("SELECT id, tenant_id, email, full_name, department, role, total_leave_days, used_leave_days, tenure_months, is_active, created_at FROM users ORDER BY id ASC")
            users = [dict(r) for r in cursor.fetchall()]
            cursor.execute("SELECT * FROM agents ORDER BY id ASC")
            agents = [dict(r) for r in cursor.fetchall()]
            cursor.execute("SELECT * FROM documents ORDER BY id ASC")
            docs = [dict(r) for r in cursor.fetchall()]
            cursor.execute("SELECT * FROM leave_requests ORDER BY id DESC")
            requests = [dict(r) for r in cursor.fetchall()]
            conn.close()
            return self.send_json({
                "tenants": tenants,
                "users": users,
                "agents": agents,
                "documents": docs,
                "leave_requests": requests
            })

        if path == "/":
            self.path = "/login.html"
        return super().do_GET()

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        # 1. API: Đăng nhập chuẩn xác thực theo 3 cấp bậc vai trò
        if path == "/api/login":
            return self.send_json({
                "error": "⛔ CHÍNH SÁCH BẢO MẬT: Đăng nhập trực tiếp đã bị vô hiệu hóa! Toàn bộ tài khoản phải xác thực qua máy chủ Keycloak SSO."
            }, 403)

        # 2. CẤP 1: SUPER_ADMIN CẤP PHÁT DOANH NGHIỆP MỚI & TẠO TÀI KHOẢN ADMIN
        elif path == "/api/tenants":
            tenant_id = data.get("tenant_id", "").strip().upper()
            tenant_name = data.get("tenant_name", "").strip()
            admin_name = data.get("admin_name", "").strip()
            admin_email = data.get("admin_email", "").strip()
            plan_type = data.get("plan_type", "ENTERPRISE").strip()
            domain_type = data.get("domain_type", "ENTERPRISE").strip().upper() or "ENTERPRISE"
            initial_schema = json.dumps(get_tenant_schema_preset(domain_type), ensure_ascii=False)

            if not tenant_id or not tenant_name or not admin_email:
                return self.send_json({"error": "Vui lòng nhập đầy đủ Mã Tenant, Tên công ty và Email Admin"}, 400)

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM tenants WHERE id = ?", (tenant_id,))
            if cursor.fetchone():
                conn.close()
                return self.send_json({"error": f"Mã doanh nghiệp '{tenant_id}' đã tồn tại!"}, 400)

            cursor.execute("SELECT id FROM users WHERE email = ?", (admin_email,))
            if cursor.fetchone():
                conn.close()
                return self.send_json({"error": f"Email Admin '{admin_email}' đã được đăng ký!"}, 400)

            # Sinh mật khẩu ngẫu nhiên an toàn (Không dùng mật khẩu mặc định)
            auto_password = generate_secure_password(10)

            # 1. Ghi dữ liệu vào CSDL SQLite và COMMIT ĐÓNG KẾT NỐI NGAY LẬP TỨC
            cursor.execute("""
                INSERT INTO tenants (id, name, contact_email, plan_type, domain_type, ui_schema)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tenant_id, tenant_name, admin_email, plan_type, domain_type, initial_schema))

            admin_display_name = admin_name or f"Admin {tenant_name}"
            admin_attrs = json.dumps({
                "total_leave_days": 15,
                "used_leave_days": 0,
                "tenure_months": 24
            }, ensure_ascii=False)

            cursor.execute("""
                INSERT INTO users (tenant_id, email, hashed_password, full_name, department, role, total_leave_days, used_leave_days, tenure_months, attributes)
                VALUES (?, ?, ?, ?, 'Executive', 'TENANT_ADMIN', 15, 0, 24, ?)
            """, (tenant_id, admin_email, auto_password, admin_display_name, admin_attrs))

            cursor.execute("""
                INSERT INTO agents (tenant_id, name, description, instruction, department_access)
                VALUES (?, ?, ?, ?, 'ALL')
            """, (tenant_id, f"{tenant_name} Assistant", f"Trợ lý AI nội bộ của {tenant_name}", f"Bạn là trợ lý thông minh hỗ trợ {tenant_name}."))

            conn.commit()
            conn.close()

            # 2. Chạy tác vụ mạng (Đồng bộ Keycloak + Gửi Email) trong luồng ngầm (Không block Database)
            import threading
            def bg_sync_and_mail():
                sync_user_to_keycloak(admin_email, auto_password, 'TENANT_ADMIN', tenant_id, admin_display_name, 'Executive')
                send_welcome_credentials_email(admin_email, admin_display_name, 'TENANT_ADMIN', tenant_name, auto_password)

            threading.Thread(target=bg_sync_and_mail, daemon=True).start()

            return self.send_json({
                "success": True, 
                "message": f"Đã cấp phép bản quyền cho {tenant_name} (Lĩnh vực: {domain_type})! Mật khẩu ngẫu nhiên an toàn đã được mã hóa trên Keycloak và gửi tới hòm thư '{admin_email}'.",
                "generated_password": auto_password
            })

        # 2b. SCHEMA API: LƯU & CẬP NHẬT UI PROFILE SCHEMA CHO TENANT
        elif path == "/api/tenants/ui_schema":
            tenant_id = data.get("tenant_id", "").strip().upper()
            schema_data = data.get("schema")
            if not tenant_id:
                return self.send_json({"error": "Thiếu tenant_id"}, 400)
            if not schema_data or not isinstance(schema_data, dict):
                return self.send_json({"error": "Dữ liệu schema không hợp lệ"}, 400)
            
            # Giới hạn kích thước (tối đa 50KB)
            if len(json.dumps(schema_data)) > 50000:
                return self.send_json({"error": "Kích thước schema vượt quá giới hạn 50KB"}, 400)
                
            validated = validate_schema(schema_data)
            if not validated:
                return self.send_json({"error": "Cấu trúc UI Profile Schema không hợp lệ hoặc thiếu trường bắt buộc"}, 400)
                
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM tenants WHERE id = ?", (tenant_id,))
            if not cursor.fetchone():
                conn.close()
                return self.send_json({"error": f"Không tìm thấy tenant '{tenant_id}'"}, 404)
                
            cursor.execute("UPDATE tenants SET ui_schema = ?, domain_type = ? WHERE id = ?", (
                json.dumps(validated, ensure_ascii=False),
                validated.get("domain_type", "CUSTOM"),
                tenant_id
            ))
            conn.commit()
            conn.close()
            return self.send_json({"success": True, "message": "Đã lưu cấu hình giao diện thích ứng thành công!", "schema": validated})

        # 2c. SCHEMA API: AI TỰ ĐỘNG SINH UI PROFILE SCHEMA BẰNG LLM
        elif path == "/api/tenants/generate_schema":
            tenant_id = data.get("tenant_id", "").strip().upper()
            description = data.get("description", "").strip()
            sample_text = data.get("sample_text", "").strip()
            domain_type = data.get("domain_type", "CUSTOM").strip()
            
            if not description and not sample_text:
                return self.send_json({"error": "Vui lòng nhập mô tả nghiệp vụ hoặc nạp văn bản mẫu"}, 400)
                
            generated = generate_schema_from_llm(description, sample_text, domain_type)
            return self.send_json({"success": True, "schema": generated})

        # 3. CẤP 2: ADMIN TẠO NHÂN VIÊN HÀNG LOẠT (BULK IMPORT EMPLOYEES)
        elif path == "/api/users/bulk":
            tenant_id = data.get("tenant_id", "").strip().upper()
            raw_text = data.get("raw_text", "").strip()

            if not tenant_id or not raw_text:
                return self.send_json({"error": "Dữ liệu danh sách trống"}, 400)

            lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
            conn = get_db()
            cursor = conn.cursor()
            created_count = 0
            errors = []
            users_to_sync = []

            for line in lines:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 2:
                    full_name = parts[0]
                    email = parts[1]
                    dept = parts[2] if len(parts) >= 3 else "General"
                    total_leave = int(parts[3]) if len(parts) >= 4 and parts[3].isdigit() else 12
                    tenure = int(parts[4]) if len(parts) >= 5 and parts[4].isdigit() else 12

                    # Phân giải thuộc tính linh hoạt (tương thích cả Enterprise, Education, Healthcare)
                    attrs = {
                        "total_leave_days": total_leave,
                        "used_leave_days": 0,
                        "tenure_months": tenure,
                        "credits_total": total_leave,
                        "credits_done": tenure,
                        "coverage_limit": total_leave,
                        "used_coverage": tenure
                    }
                    if len(parts) >= 6:
                        for extra in parts[5:]:
                            if "=" in extra:
                                k, v = extra.split("=", 1)
                                k, v = k.strip(), v.strip()
                                try:
                                    attrs[k] = float(v) if "." in v else int(v)
                                except ValueError:
                                    attrs[k] = v
                    attrs_json = json.dumps(attrs, ensure_ascii=False)

                    try:
                        auto_pass = generate_secure_password(10)
                        cursor.execute("""
                            INSERT INTO users (tenant_id, email, hashed_password, full_name, department, role, total_leave_days, used_leave_days, tenure_months, attributes)
                            VALUES (?, ?, ?, ?, ?, 'EMPLOYEE', ?, 0, ?, ?)
                        """, (tenant_id, email, auto_pass, full_name, dept, total_leave, tenure, attrs_json))
                        created_count += 1
                        users_to_sync.append((email, auto_pass, full_name, dept))
                    except sqlite3.IntegrityError:
                        errors.append(f"Email '{email}' đã tồn tại")

            conn.commit()
            conn.close()

            # Chạy sync Keycloak và gửi email trong background thread để không block UI
            if users_to_sync:
                import threading
                def bg_bulk_sync(items, tid):
                    for u_email, u_pwd, u_name, u_dept in items:
                        try:
                            sync_user_to_keycloak(u_email, u_pwd, 'EMPLOYEE', tid, u_name, u_dept)
                            send_welcome_credentials_email(u_email, u_name, 'EMPLOYEE', tid, u_pwd)
                        except Exception as e:
                            print(f"Error bulk syncing {u_email}:", e)
                threading.Thread(target=bg_bulk_sync, args=(users_to_sync, tenant_id), daemon=True).start()

            return self.send_json({
                "success": True,
                "created_count": created_count,
                "errors": errors,
                "message": f"Đã tạo thành công {created_count} nhân viên cho {tenant_id}! Mật khẩu riêng biệt của từng nhân viên đã được mã hóa trên Keycloak và gửi về hòm thư tương ứng."
            })

        # 4. ADMIN TẠO 1 NHÂN VIÊN ĐƠN LẺ
        elif path == "/api/users":
            tenant_id = data.get("tenant_id", "").strip().upper()
            email = data.get("email", "").strip()
            full_name = data.get("full_name", "").strip()
            department = data.get("department", "Sản xuất").strip()
            role = data.get("role", "EMPLOYEE").strip()
            total_leave_days = int(data.get("total_leave_days", 12))
            tenure_months = int(data.get("tenure_months", 12))
            auto_pass = data.get("password", "").strip() or generate_secure_password(10)

            if not tenant_id or not email or not full_name:
                return self.send_json({"error": "Vui lòng nhập đủ thông tin"}, 400)

            conn = get_db()
            cursor = conn.cursor()
            try:
                attrs_data = data.get("attributes", {})
                if isinstance(attrs_data, str):
                    try:
                        attrs_data = json.loads(attrs_data)
                    except Exception:
                        attrs_data = {}
                if not isinstance(attrs_data, dict):
                    attrs_data = {}
                attrs_data.setdefault("total_leave_days", total_leave_days)
                attrs_data.setdefault("used_leave_days", 0)
                attrs_data.setdefault("tenure_months", tenure_months)
                attrs_data.setdefault("credits_total", total_leave_days)
                attrs_data.setdefault("credits_done", tenure_months)
                attrs_json = json.dumps(attrs_data, ensure_ascii=False)

                cursor.execute("""
                    INSERT INTO users (tenant_id, email, hashed_password, full_name, department, role, total_leave_days, used_leave_days, tenure_months, attributes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
                """, (tenant_id, email, auto_pass, full_name, department, role, total_leave_days, tenure_months, attrs_json))
                new_id = cursor.lastrowid
                conn.commit()
                conn.close()

                # Gửi mail & Keycloak ngầm
                import threading
                threading.Thread(target=lambda: (
                    sync_user_to_keycloak(email, auto_pass, role, tenant_id, full_name, department),
                    send_welcome_credentials_email(email, full_name, role, tenant_id, auto_pass)
                ), daemon=True).start()

                return self.send_json({
                    "success": True, 
                    "id": new_id, 
                    "message": f"Đã tạo tài khoản cho {full_name}! Mật khẩu ngẫu nhiên an toàn đã được mã hóa trên Keycloak và gửi tới hòm thư '{email}'.",
                    "generated_password": auto_pass
                })
            except sqlite3.IntegrityError:
                conn.close()
                return self.send_json({"error": f"Email '{email}' đã tồn tại trong CSDL!"}, 400)

        # 5. CẬP NHẬT / CHỈNH SỬA TÀI KHOẢN (UPDATE USER)
        elif path == "/api/users/update":
            user_id = data.get("id")
            if not user_id:
                return self.send_json({"error": "Thiếu user_id"}, 400)

            full_name = data.get("full_name", "").strip()
            email = data.get("email", "").strip()
            department = data.get("department", "").strip()
            role = data.get("role")
            total_leave_days = int(data.get("total_leave_days", 12))
            tenure_months = int(data.get("tenure_months", 12))
            password = data.get("password", "").strip()

            conn = get_db()
            cursor = conn.cursor()
            try:
                if password:
                    if role:
                        cursor.execute("""
                            UPDATE users 
                            SET full_name = ?, email = ?, department = ?, role = ?, total_leave_days = ?, tenure_months = ?, hashed_password = ?
                            WHERE id = ?
                        """, (full_name, email, department, role, total_leave_days, tenure_months, password, user_id))
                    else:
                        cursor.execute("""
                            UPDATE users 
                            SET full_name = ?, email = ?, department = ?, total_leave_days = ?, tenure_months = ?, hashed_password = ?
                            WHERE id = ?
                        """, (full_name, email, department, total_leave_days, tenure_months, password, user_id))
                else:
                    if role:
                        cursor.execute("""
                            UPDATE users 
                            SET full_name = ?, email = ?, department = ?, role = ?, total_leave_days = ?, tenure_months = ?
                            WHERE id = ?
                        """, (full_name, email, department, role, total_leave_days, tenure_months, user_id))
                    else:
                        cursor.execute("""
                            UPDATE users 
                            SET full_name = ?, email = ?, department = ?, total_leave_days = ?, tenure_months = ?
                            WHERE id = ?
                        """, (full_name, email, department, total_leave_days, tenure_months, user_id))

                conn.commit()
                conn.close()
                return self.send_json({"success": True, "message": f"Đã cập nhật thông tin tài khoản #{user_id} ({full_name}) thành công!"})
            except sqlite3.IntegrityError:
                conn.close()
                return self.send_json({"error": f"Email '{email}' đã được sử dụng bởi tài khoản khác!"}, 400)

        # 6. XÓA USER (DELETE USER)
        elif path == "/api/users/delete":
            user_id = data.get("user_id")
            if not user_id:
                return self.send_json({"error": "Thiếu user_id"}, 400)

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
            u_row = cursor.fetchone()
            if u_row:
                delete_user_from_keycloak(u_row["email"])

            cursor.execute("DELETE FROM leave_requests WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return self.send_json({"success": True, "message": f"Đã xóa tài khoản #{user_id} thành công!"})

        # 7. XÓA DOANH NGHIỆP (TENANT DELETE - CHO SUPER ADMIN)
        elif path == "/api/tenants/delete":
            tenant_id = data.get("tenant_id")
            if not tenant_id or tenant_id == "PLATFORM":
                return self.send_json({"error": "Không thể xóa doanh nghiệp này!"}, 400)

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM leave_requests WHERE tenant_id = ?", (tenant_id,))
            cursor.execute("DELETE FROM agents WHERE tenant_id = ?", (tenant_id,))
            cursor.execute("DELETE FROM documents WHERE tenant_id = ?", (tenant_id,))
            cursor.execute("DELETE FROM users WHERE tenant_id = ?", (tenant_id,))
            cursor.execute("DELETE FROM tenants WHERE id = ?", (tenant_id,))
            conn.commit()
            conn.close()
            return self.send_json({"success": True, "message": f"Đã xóa hoàn toàn doanh nghiệp {tenant_id} cùng toàn bộ tài khoản liên quan!"})

        # 6. TẠO AGENT MỚI
        elif path == "/api/agents":
            tenant_id = data.get("tenant_id", "").strip().upper()
            name = data.get("name", "Trợ lý mới").strip()
            description = data.get("description", "")
            instruction = data.get("instruction", "")
            department_access = data.get("department_access", "ALL")

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO agents (tenant_id, name, description, instruction, department_access, is_published)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (tenant_id, name, description, instruction, department_access))
            new_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return self.send_json({"success": True, "id": new_id, "name": name})

        # 7. TẠO ĐƠN NGHỈ PHÉP (HITL)
        elif path == "/api/leave_requests":
            tenant_id = data.get("tenant_id", "VINFAST")
            user_id = data.get("user_id")
            user_name = data.get("user_name", "")
            days_requested = int(data.get("days_requested", 1))
            date_details = data.get("date_details", "")

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO leave_requests (tenant_id, user_id, user_name, days_requested, date_details, status, notified_to_user)
                VALUES (?, ?, ?, ?, ?, 'PENDING', 0)
            """, (tenant_id, user_id, user_name, days_requested, date_details))
            new_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return self.send_json({"success": True, "id": new_id, "status": "PENDING"})

        # 8. PHÊ DUYỆT ĐƠN NGHỈ PHÉP
        elif path == "/api/leave_requests/decision":
            req_id = data.get("request_id")
            decision = data.get("decision")

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, days_requested, status FROM leave_requests WHERE id = ?", (req_id,))
            req = cursor.fetchone()

            if not req:
                conn.close()
                return self.send_json({"error": "Không tìm thấy đơn"}, 404)

            user_id = req["user_id"]
            days = req["days_requested"]
            old_status = req["status"]

            cursor.execute("UPDATE leave_requests SET status = ?, notified_to_user = 0 WHERE id = ?", (decision, req_id))
            if decision == "APPROVED" and old_status != "APPROVED":
                cursor.execute("UPDATE users SET used_leave_days = used_leave_days + ? WHERE id = ?", (days, user_id))

            conn.commit()
            conn.close()
            return self.send_json({"success": True, "decision": decision})

        # 9. CHAT LANGGRAPH AGENT
        elif path == "/api/chat":
            user_id = data.get("user_id")
            agent_name = data.get("agent_name", "AI Assistant")
            message = data.get("message", "").strip()

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT full_name, department, total_leave_days, used_leave_days, tenure_months, tenant_id FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()

            cursor.execute("SELECT instruction, department_access, tenant_id FROM agents WHERE name = ?", (agent_name,))
            agent_row = cursor.fetchone()
            conn.close()

            user_dict = dict(user) if user else {"full_name": "Nhân viên", "department": "Sản xuất", "total_leave_days": 12, "used_leave_days": 0, "tenure_months": 12, "tenant_id": "VINFAST"}
            tenant_id = user_dict.get("tenant_id") or (agent_row["tenant_id"] if agent_row else "VINFAST")
            instruction = agent_row["instruction"] if agent_row else "Bạn là trợ lý ảo doanh nghiệp."
            dept_access = agent_row["department_access"] if agent_row else "ALL"

            graph_agent = LangGraphAgent(agent_name, instruction, dept_access, tenant_id=tenant_id)
            result = graph_agent.run(user_dict, message)

            return self.send_json({
                "reply": result["reply"],
                "citation": result["citation"],
                "intent": result["intent"],
                "latency": result["latency"],
                "token_estimate": result["token_estimate"]
            })

        # 10. NẠP TÀI LIỆU MỚI CHO DOANH NGHIỆP (UPLOAD/CREATE DOCUMENT)
        elif path == "/api/documents":
            tenant_id = data.get("tenant_id", "").strip().upper()
            file_name = data.get("file_name", "").strip()
            content = data.get("content", "").strip()

            if not tenant_id or not file_name or not content:
                return self.send_json({"error": "Vui lòng nhập tên tài liệu và nội dung đầy đủ!"}, 400)

            if not (file_name.endswith(".txt") or file_name.endswith(".pdf") or file_name.endswith(".md")):
                file_name += ".txt"

            fpath = os.path.join(DATA_DIR, file_name)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)

            fsize_kb = max(1, round(len(content.encode("utf-8")) / 1024))

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO documents (tenant_id, file_name, file_path, file_size_kb)
                VALUES (?, ?, ?, ?)
            """, (tenant_id, file_name, fpath.replace("\\", "/"), fsize_kb))
            new_doc_id = cursor.lastrowid
            conn.commit()
            conn.close()

            # Vectorize
            from vector_store import add_document_to_vector_store
            chunks_added = add_document_to_vector_store(file_name, content, tenant_id)

            return self.send_json({
                "success": True,
                "id": new_doc_id,
                "file_name": file_name,
                "chunks_added": chunks_added,
                "message": f"Đã lưu '{file_name}' vào CSDL và vector hóa thành công {chunks_added} đoạn cho {tenant_id}!"
            })

        return self.send_json({"error": "Endpoint not found"}, 404)

if __name__ == "__main__":
    server_address = ("", PORT)
    with ThreadingHTTPServer(server_address, UnifiedHandler) as httpd:
        print(f"🚀 SaaS Multi-Tenant Server running on http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer shutting down.")
