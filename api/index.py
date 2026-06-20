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
    await update.message.reply_text("""✅ **MyHackLearnerBot চালু আছে!**

শিখতে চাও যেকোনো একটা লিখো:
• python hacking
• sql injection
• xss
• reverse shell
• wifi cracking""")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    
    text = update.message.text.lower().strip()
    
    if "python" in text:
        reply = "🐍 Python Hacking Scripts চাইলে বলো 'portscan' বা 'revshell'"
    elif "sql" in text or "injection" in text:
        reply = "💉 SQL Injection:\n' OR '1'='1' --\nDVWA তে প্র্যাকটিস করো"
    elif "xss" in text:
        reply = "❌ XSS Payload:\n<script>alert('Hacked')</script>"
    elif "reverse" in text or "shell" in text:
        reply = "🔄 Python Reverse Shell কোড চাইলে 'revshell' লিখো"
    elif "wifi" in text:
        reply = "📡 WiFi Cracking steps চাইলে 'wifi' লিখো"
    else:
        reply = "✅ বট চালু আছে! কোন টপিক শিখতে চাও?"
    
    await update.message.reply_text(reply)

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        if not application._initialized:
            await application.initialize()
        await application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        print("Error:", str(e))
        return {"status": "error"}

@app.get("/")
async def home():
    return {"message": "✅ Bot is Live!"}
