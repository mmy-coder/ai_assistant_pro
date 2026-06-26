import os
import PyPDF2
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI

# ==================== DeepSeek 客户端配置（修改就在这里） ====================
# 请将下方的密钥替换为你在 platform.deepseek.com 生成的 Key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",  # DeepSeek 的官方 API 地址
)
# ============================================================================

app = FastAPI(title="AI 智能助手")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


# ================= Pydantic 数据模型 =================
class ChatRequest(BaseModel):
    message: str


class TranslateRequest(BaseModel):
    text: str
    target_lang: str


class WriteRequest(BaseModel):
    prompt: str


# ================= 核心 AI 业务路由 =================


# 1. AI 智能聊天
@app.post("/api/chat")
async def ai_chat(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # 指定 DeepSeek 模型
            messages=[{"role": "user", "content": req.message}],
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(500, f"调用失败: {str(e)}")


# 2. AI 翻译
@app.post("/api/translate")
async def ai_translate(req: TranslateRequest):
    try:
        prompt = f"请将以下文本翻译成{req.target_lang}，只返回翻译结果：\n{req.text}"
        response = client.chat.completions.create(
            model="deepseek-chat", messages=[{"role": "user", "content": prompt}]
        )
        return {"translation": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(500, f"翻译失败: {str(e)}")


# 3. AI 总结 PDF（含文档解析）
@app.post("/api/summarize")
async def ai_summarize_pdf(file: UploadFile = File(...)):
    try:
        content = await file.read()
        pdf_reader = PyPDF2.PdfReader(content)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        if len(text) < 10:
            raise HTTPException(400, "PDF 内容为空或无法解析文字")

        text = text[:8000]  # 截断文本防止超出 Token 限制

        prompt = f"请根据以下文本内容，生成一份结构清晰的总结摘要，包含核心观点和结论：\n\n{text}"
        response = client.chat.completions.create(
            model="deepseek-chat", messages=[{"role": "user", "content": prompt}]
        )
        return {"summary": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(500, f"PDF解析或总结失败: {str(e)}")


# 4. AI 写作助手
@app.post("/api/write")
async def ai_write(req: WriteRequest):
    try:
        prompt = f"请根据我的提示，帮我写一篇内容。要求：条理清晰，语言流畅，重点突出。提示如下：\n{req.prompt}"
        response = client.chat.completions.create(
            model="deepseek-chat", messages=[{"role": "user", "content": prompt}]
        )
        return {"content": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(500, f"写作失败: {str(e)}")


# ================= 托管网页 =================
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
