# 🚀 AI20K - CHAT-40: Mini Agent Studio
> **Đội thi:** T057 | **Khóa học:** Phoenix AI20K - Cohort V  
> **Lĩnh vực:** Chat – Ứng dụng nhắn tin & Cộng tác doanh nghiệp  
> **Đề tài:** CHAT-40 — Mini Agent Studio – Tạo AI Agent không cần lập trình (No-Code AI Agent Platform)

---

## 📌 Giới thiệu dự án (Overview)
**Mini Agent Studio** là nền tảng Self-service / No-Code cho phép các phòng ban nghiệp vụ (HR, CSKH, Sales, Quản lý nội bộ) tự cấu hình, thử nghiệm và xuất bản các AI Agent chuyên biệt chỉ trong vài phút mà **hoàn toàn không cần kỹ năng lập trình**.

Hệ thống giải quyết triệt để các bài toán thực tế của doanh nghiệp:
- 📑 **Knowledge Base (RAG):** Nạp tài liệu nội bộ (.PDF, .DOCX, FAQ), tự động dẫn nguồn chính xác (Citations).
- ⚙️ **Workflow 3–5 Node (React Flow):** Trực quan hóa luồng xử lý bằng kéo thả.
- 🛠️ **Tích hợp Tools & Actions:** Tra cứu dữ liệu, tính toán, gửi yêu cầu tự động.
- 🛡️ **Bảo mật & Phân quyền (ACL, HITL):** Xác nhận hành động nhạy cảm của người dùng (Human-in-the-loop), cô lập dữ liệu doanh nghiệp và che giấu PII.
- 📊 **Giám sát & Đánh giá (Observability):** Tích hợp Langfuse để đo lường Latency, Token Cost, và chất lượng truy hồi.

---

## 🏗️ Kiến trúc hệ thống (System Architecture)

```text
[ Người dùng / Creator ]
         │ (Giao diện Kéo thả React Flow / Web Studio)
         ▼
[ Frontend Studio (Port 3000 / 8501) ]
         │ (RESTful API / WebSocket)
         ▼
[ Backend API Gateway - FastAPI (Port 8000) ]
   ├── 🔐 Auth & ACL (Phân quyền truy cập tài liệu)
   ├── 🧠 LangGraph Engine (State Graph điều phối luồng xử lý)
   │     ├── Node 1: Router / Intent Classifier
   │     ├── Node 2: Document Retriever (Qdrant Vector DB)
   │     ├── Node 3: Tool Executor (≥ 3 Tools)
   │     └── Node 4: Human-in-the-loop Interrupt (Xác nhận thao tác nhạy cảm)
   ├── 🗄️ Database: PostgreSQL / SQLite (Quản lý Bot, Session, Chat logs)
   └── 📈 Observability: Langfuse (Tracing, Metrics, Cost monitoring)
```

---

## 📁 Cấu trúc thư mục (Directory Structure)

```text
AI20K_T057_CHAT_40_Mini-Agent-Studio/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI Endpoints (Agents, Documents, Chat, Tools)
│   │   ├── core/            # Config, Security, Environment settings
│   │   ├── engine/          # LangGraph Workflow, State Graph, Memory
│   │   ├── rag/             # PDF Parser, Chunking, Vector Embeddings (Qdrant)
│   │   ├── tools/           # Custom Tools (Leave Calculation, Calendar, Approval)
│   │   └── models/          # Database ORM Models & Schemas
│   ├── requirements.txt     # Python Dependencies
│   └── main.py              # Server Entrypoint
├── frontend/                # Web Studio UI (React Flow / Streamlit Studio)
├── docs/                    # Tài liệu nộp Gate 1-3, Slide thuyết trình Demo Day
├── data/                    # Tài liệu mẫu (Sample PDF: Nội quy, Chính sách)
└── README.md                # Tài liệu hướng dẫn sử dụng
```

---

## 👥 Phân công nhiệm vụ nhóm (Team Roles)

| Thành viên | Vai trò | Trách nhiệm chính |
| :--- | :--- | :--- |
| **Đỗ Lý Hoàng Nam** | **Team Leader / Product Manager** | Quản lý tiến độ dự án, thiết kế nghiệp vụ, cơ chế Human-in-the-loop, bảo mật ACL và thuyết trình Demo Day. |
| **Thành viên 2** | **AI Engine Lead** | Xây dựng LangGraph State Machine, tích hợp LLM API, viết code 3 Tools và bài toán tách luồng hội thoại. |
| **Thành viên 3** | **Fullstack & UI Engineer** | Phát triển giao diện Web Studio, bảng vẽ kéo thả React Flow và khung chat Sandbox. |
| **Thành viên 4** | **Data & MLOps Engineer** | Cấu hình Vector DB (Qdrant), tích hợp Langfuse Tracing và chạy đánh giá Benchmark định lượng. |

---

## ⚡ Hướng dẫn cài đặt nhanh (Quickstart)

### 1. Yêu cầu môi trường
- Python 3.10+
- Git

### 2. Cài đặt Backend
```bash
cd backend
python -m venv venv
# Kích hoạt venv trên Windows:
venv\Scripts\activate
# Cài đặt thư viện:
pip install -r requirements.txt
# Khởi chạy server:
python main.py
```
API Docs Swagger sẽ chạy tại: `http://localhost:8000/docs`

---
*© 2026 Team T057 - Phoenix AI20K Cohort V. All rights reserved.*
