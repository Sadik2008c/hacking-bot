from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

app = FastAPI()

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", 0))

application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ এই বট শুধু Owner এর জন্য।")
        return
    await update.message.reply_text("""🔥 **Educational Hacking Learning Bot**

মেনু:
• python hacking
• sql injection
• xss
• reverse shell
• wifi cracking
• ctf""")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    
    text = update.message.text.lower().strip()
    
    if "python" in text and "hacking" in text:
        reply = "🐍 Python Port Scanner কোড:\n```python\nimport socket\ntarget = '192.168.1.1'\nfor port in range(1,100):\n    s = socket.socket()\n    if s.connect_ex((target, port)) == 0:\n        print(f'Port {port} open')\n```"
    elif "sql" in text or "injection" in text:
        reply = "💉 SQL Injection Payload:\n' OR '1'='1' --"
    elif "xss" in text:
        reply = "❌ XSS Payload:\n<script>alert('Hacked')</script>"
    elif "reverse" in text or "shell" in text:
        reply = "🔄 Reverse Shell কোড চাইলে 'revshell' লিখো"
    elif "wifi" in text:
        reply = "📡 WiFi Cracking steps চাইলে 'wifi steps' লিখো"
    else:
        reply = "ঠিক আছে! আরও বিস্তারিত জানতে টপিকের নাম লিখো।"
    
    await update.message.reply_text(reply)

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        print(e)
        return {"status": "error"}

@app.get("/")
async def home():
    return {"message": "✅ Educational Hacking Bot is Live on Vercel!"}
