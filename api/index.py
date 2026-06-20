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
• wifi cracking
• ctf
• metasploit""")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    
    text = update.message.text.lower().strip()
    
    if "python" in text and "hacking" in text:
        reply = """🐍 **Python Hacking Scripts:**

**Port Scanner:**
```python
import socket
target = "192.168.0.1"
for port in range(1, 500):
    s = socket.socket()
    if s.connect_ex((target, port)) == 0:
        print(f"Port {port} Open")
    s.close()
