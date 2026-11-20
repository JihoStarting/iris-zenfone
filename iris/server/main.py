# Iris Fase 2 - server otak (FastAPI) - by: KangJiho
# Jalankan dari folder iris/ (bukan dari server/):  uvicorn server.main:app --host 0.0.0.0 --port 8000
import os, json
import httpx
from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Default diarahkan ke 9Router (jalan di WSL, harus dinyalakan dulu). Ganti lewat variabel lingkungan.
BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:20128/v1")
API_KEY = os.getenv("LLM_API_KEY", "")
MODEL = os.getenv("LLM_MODEL", "Iris")      # nama combo di 9Router; sesuaikan kalau beda
TOKEN = os.getenv("IRIS_TOKEN", "")         # kata sandi bebas, wajib diisi
HIST_FILE = "memory.json"
PERSONA = (
    "Kamu Iris, teman virtual yang hangat dan singkat. "
    "Balas dalam bahasa Indonesia, maksimal 3 kalimat, tanpa emoji dan tanpa markdown "
    "karena jawabanmu akan dibacakan oleh suara."
)

app = FastAPI()


class Msg(BaseModel):
    text: str


def load():
    try:
        with open(HIST_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save(h):
    with open(HIST_FILE, "w", encoding="utf-8") as f:
        json.dump(h[-200:], f, ensure_ascii=False)


@app.get("/ping")
def ping():
    return {"ok": True}


@app.post("/chat")
async def chat(m: Msg, x_token: str = Header(default="")):
    if not TOKEN or x_token != TOKEN:
        raise HTTPException(status_code=401)
    hist = load()
    hist.append({"role": "user", "content": m.text[:1000]})
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    try:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(
                f"{BASE_URL}/chat/completions",
                headers=headers,
                json={
                    "model": MODEL,
                    "max_tokens": 300,
                    "messages": [{"role": "system", "content": PERSONA}] + hist[-20:],
                },
            )
        r.raise_for_status()
        reply = r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("LLM error:", repr(e))
        raise HTTPException(status_code=502, detail="LLM gagal")
    hist.append({"role": "assistant", "content": reply})
    save(hist)
    return {"reply": reply}


# Harus paling bawah, setelah semua route
app.mount("/", StaticFiles(directory="web", html=True), name="web")
