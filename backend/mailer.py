import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os

# 1. HÀM SINH MẬT KHẨU NGẪU NHIÊN BẢO MẬT CAO
def generate_secure_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = ''.join(secrets.choice(chars) for _ in range(length))
        if (any(c.islower() for c in password) and 
            any(c.isupper() for c in password) and 
            any(c.isdigit() for c in password) and
            any(c in "!@#$%^&*" for c in password)):
            return password

# 2. CẤU HÌNH GOOGLE GMAIL SMTP CỐ ĐỊNH CHO HỆ THỐNG
def _load_env():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
_load_env()

SMTP_CONFIG = {
    "host": "smtp.gmail.com",
    "port": 465,
    "user": os.environ.get("SMTP_USER", ""),
    "pass": os.environ.get("SMTP_PASS", ""),  # Google App Password (đọc từ backend/.env)
    "sender_name": "Mini Agent Studio Platform"
}

LOG_DIR = os.path.abspath(os.path.dirname(__file__))
EMAIL_LOG_FILE = os.path.join(LOG_DIR, "sent_emails.log")

# 3. HÀM TỰ ĐỘNG GỬI EMAIL BÀN GIAO MẬT KHẨU
def send_welcome_credentials_email(recipient_email, full_name, role, tenant_name, raw_password, smtp_config=None):
    cfg = smtp_config or SMTP_CONFIG
    subject = f"[{tenant_name}] Bàn giao tài khoản quản trị & Mật khẩu đăng nhập hệ thống"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #111827; background: #f8fafc; padding: 24px; }}
            .card {{ max-width: 580px; margin: 0 auto; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 36px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
            .brand {{ font-size: 13px; font-weight: 700; letter-spacing: 0.05em; color: #0f172a; text-transform: uppercase; margin-bottom: 8px; }}
            .title {{ font-size: 22px; font-weight: 800; color: #09090b; margin: 0 0 16px 0; letter-spacing: -0.02em; }}
            .cred-box {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 20px; margin: 24px 0; }}
            .cred-row {{ margin-bottom: 10px; font-size: 14px; display: flex; align-items: center; justify-content: space-between; }}
            .cred-label {{ color: #64748b; font-weight: 500; }}
            .cred-val {{ font-family: 'Courier New', Courier, monospace; font-size: 15px; font-weight: 700; color: #09090b; background: #e2e8f0; padding: 4px 10px; border-radius: 6px; letter-spacing: 0.05em; }}
            .btn {{ display: block; text-align: center; background: #000000; color: #ffffff !important; padding: 14px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 14px; margin-top: 24px; }}
            .note {{ font-size: 12px; color: #ef4444; margin-top: 16px; line-height: 1.5; }}
            .footer {{ font-size: 11px; color: #94a3b8; margin-top: 32px; border-top: 1px solid #f1f5f9; padding-top: 16px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="brand">MINI AGENT STUDIO • ENTERPRISE IAM</div>
            <h1 class="title">Xin chào {full_name},</h1>
            
            <p style="font-size: 14px; color: #334155; line-height: 1.6;">
                Tổ chức <strong>{tenant_name}</strong> đã cấp quyền tài khoản cho bạn trên nền tảng với vai trò: <strong>{role}</strong>.
            </p>

            <div class="cred-box">
                <div class="cred-row">
                    <span class="cred-label">Cổng đăng nhập SSO:</span>
                    <span style="font-size: 13px; font-weight: 600;">http://localhost:8000/login.html</span>
                </div>
                <div class="cred-row">
                    <span class="cred-label">Tài khoản (Email):</span>
                    <span class="cred-val">{recipient_email}</span>
                </div>
                <div class="cred-row">
                    <span class="cred-label">Mật khẩu khởi tạo:</span>
                    <span class="cred-val" style="color: #2563eb; background: #eff6ff;">{raw_password}</span>
                </div>
            </div>

            <p class="note">
                🔒 <strong>Chính sách bảo mật:</strong> Mật khẩu này được sinh ngẫu nhiên và mã hóa trực tiếp bởi máy chủ Keycloak SSO. Trong lần đầu tiên đăng nhập, hệ thống sẽ yêu cầu bạn đổi sang mật khẩu cá nhân để bảo vệ tài khoản.
            </p>

            <a href="http://localhost:8000/login.html" class="btn">Đăng nhập vào Hệ thống ngay</a>

            <div class="footer">
                Email này được gửi tự động từ máy chủ điều hành Mini Agent Studio Platform.<br>
                Quản trị bởi Super Admin: dolyhoangnam13072005@gmail.com
            </div>
        </div>
    </body>
    </html>
    """

    # Ghi log
    log_entry = f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SENT TO: {recipient_email} | NAME: {full_name} | TENANT: {tenant_name} | ROLE: {role} | PASS: {raw_password}\n"
    with open(EMAIL_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

    # Gửi qua Google Gmail SMTP SSL
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f'"{cfg.get("sender_name", "Mini Agent Studio")}" <{cfg["user"]}>'
        msg["To"] = recipient_email
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP_SSL(cfg["host"], cfg["port"], timeout=15) as server:
            server.login(cfg["user"], cfg["pass"])
            server.sendmail(cfg["user"], [recipient_email], msg.as_string())
        
        print(f"🚀 [GMAIL REAL DELIVERY SUCCESS] Email sent to {recipient_email}!")
        return True, "Email đã được gửi thành công đến hòm thư thực tế!"
    except Exception as e:
        print(f"⚠️ [SMTP ERROR] Could not deliver email to {recipient_email}: {e}")
        return False, str(e)
