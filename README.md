# ✨ AI 智能助手 (Apple 暗黑风)

基于 FastAPI 与 DeepSeek API 构建的多功能 AI 工具箱，集成聊天、翻译、文档总结与写作功能。

**核心功能**：
- 💬 **AI 聊天**：使用 DeepSeek 大语言模型进行自然对话。
- 🌍 **AI 翻译**：支持任意语言智能翻译。
- 📄 **AI 总结 PDF**：支持拖拽上传 PDF，自动提取核心信息生成摘要。
- ✍️ **AI 写作助手**：根据关键词或主题，生成高质量文案、信件、计划书等。

**技术栈**：
- 后端：FastAPI, DeepSeek SDK, PyPDF2 文档解析
- 前端：SPA 多标签架构, 原生 HTML/CSS/JS
- 部署：cpolar 内网穿透

**重要运行说明**：
1. 本项目使用 DeepSeek API，**无需翻墙**。
2. 请在 `main.py` 文件头部替换你的 DeepSeek API Key：`DEEPSEEK_API_KEY = "sk-你的密钥"`

**启动步骤**：
1. 安装依赖：`pip install fastapi uvicorn pymysql python-multipart openai PyPDF2`
2. 启动后端：`uvicorn main:app --reload`
3. 访问：`http://127.0.0.1:8000`