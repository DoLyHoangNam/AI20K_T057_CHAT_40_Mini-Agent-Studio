import os
import json
import urllib.request
import math
import time
from typing import List, Dict, Any

API_KEY = os.environ.get("GEMINI_API_KEY", "")
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
INDEX_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "vector_index.json"))

def get_embedding(text: str) -> List[float]:
    if not API_KEY:
        return []
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key={API_KEY}"
    payload = {
        "model": "models/gemini-embedding-001",
        "content": {"parts": [{"text": text[:2000]}]}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))
            return data["embedding"]["values"]
    except Exception as e:
        print(f"Lỗi embedding: {e}")
        return []

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a, v in zip(v1, v1)))
    norm2 = math.sqrt(sum(b * b for b, b in zip(v2, v2)))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def build_vector_store():
    print("🔄 Đang xây dựng Vector Database cô lập theo Multi-Tenant...")
    chunks_data = []

    file_tenant_map = {
        "Noi_quy_Phong_Marketing_VinFast.txt": "VINFAST",
        "Quy_che_Nhan_su_VinFast_2026.txt": "VINFAST",
        "Quy_che_Tai_chinh_Ke_toan.txt": "VINFAST",
        "Quy_che_Lam_viec_FPT_Software.txt": "FPT",
        "Quy_che_VNG_Games_2026.txt": "VNG"
    }

    for fname, tenant_id in file_tenant_map.items():
        fpath = os.path.join(DATA_DIR, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        paragraphs = [p.strip() for p in content.split("\n\n") if len(p.strip()) > 25]
        for idx, p in enumerate(paragraphs):
            print(f"  Vector hóa [{tenant_id}]: {fname} [Chunk {idx+1}/{len(paragraphs)}]...")
            emb = get_embedding(p)
            if emb:
                chunks_data.append({
                    "id": f"{fname}_{idx}",
                    "tenant_id": tenant_id,
                    "source": fname,
                    "text": p,
                    "vector": emb
                })

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks_data, f, ensure_ascii=False)
    print(f"✅ Đã hoàn tất nạp {len(chunks_data)} Vectors cô lập theo Tenant!")

def vector_search(query: str, tenant_id: str = "VINFAST", department_access: str = "ALL", top_k: int = 2) -> List[Dict[str, Any]]:
    if not os.path.exists(INDEX_FILE):
        build_vector_store()

    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            chunks = json.load(f)
    except Exception:
        return []

    q_vec = get_embedding(query)
    if not q_vec:
        return []

    scored_chunks = []
    for c in chunks:
        # BẢO MẬT CÔ LẬP TENANT TUYỆT ĐỐI: Chỉ tìm tài liệu thuộc đúng Tenant của công ty đó!
        chunk_tenant = c.get("tenant_id", "VINFAST")
        if tenant_id != "PLATFORM" and chunk_tenant != tenant_id:
            continue

        sim = cosine_similarity(q_vec, c["vector"])
        scored_chunks.append({
            "text": c["text"],
            "source": c["source"],
            "tenant_id": chunk_tenant,
            "score": sim
        })

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:top_k]

def add_document_to_vector_store(file_name: str, content: str, tenant_id: str) -> int:
    """Nạp thêm 1 tài liệu mới và vector hóa lưu trữ cô lập theo Tenant"""
    if not os.path.exists(INDEX_FILE):
        build_vector_store()

    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            chunks_data = json.load(f)
    except Exception:
        chunks_data = []

    # Xóa các chunk cũ của file này nếu có
    chunks_data = [c for c in chunks_data if not (c.get("source") == file_name and c.get("tenant_id") == tenant_id)]

    paragraphs = [p.strip() for p in content.split("\n\n") if len(p.strip()) > 20]
    added = 0
    for idx, p in enumerate(paragraphs):
        emb = get_embedding(p)
        if emb:
            chunks_data.append({
                "id": f"{file_name}_{idx}_{int(time.time())}",
                "tenant_id": tenant_id,
                "source": file_name,
                "text": p,
                "vector": emb
            })
            added += 1

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks_data, f, ensure_ascii=False)

    return added

if __name__ == "__main__":
    build_vector_store()
