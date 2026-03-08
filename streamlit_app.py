import streamlit as st
import asyncio
import threading
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# --- ظاهر داشبورد ---
st.set_page_config(page_title="Rasul Coach", page_icon="🦁")
st.title("🦁 مربی مقتدر رسول آقا خوشناو")
st.write("وضعیت: در حال نظارت بر اهداف ۳ ماهه")

# --- کلیدهای امنیتی ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
GEMINI_API_KEY = 'AIzaSyA_ZLJg38IuBcTkIM0cK4oV06xNer98Vto'

genai.configure(api_key=GEMINI_API_KEY)
# استفاده از مدل فلش که در اربیل و سرورهای ابری عالی جواب می‌دهد
model = genai.GenerativeModel('gemini-1.5-flash')

SOUL_PROMPT = """
تۆ «مربی»یت، مربی شخصی، برنامه‌ریز قاطع و مشوق رسول آقا (رسول صالح خوشناو) لە هەولێر.
اهداف ۳ ماهه: ۱. نامه‌نگاری اداری ٢. ویزیتوری ۳. اتیکت.
وظیفه: مبارزه با تیک‌تاک و تنبلی.
همیشه با «رسول آقا، خب، بیا برویم!» شروع کن.
"""

async def handle_message(update: Update, context):
    if not update.message or not update.message.text: return
    try:
        response = model.generate_content(f"{SOUL_PROMPT}\n\nرسول آقا: {update.message.text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"رسول آقا قهرمان، مربی بیدار است اما مغز گوگل کمی کُند شده. دوباره بگویید!")

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # اضافه کردن یک وقفه کوتاه برای حل مشکل Conflict
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(stop_signals=None, close_loop=False)

if "bot_started" not in st.session_state:
    st.session_state.bot_started = True
    threading.Thread(target=start_bot, daemon=True).start()
    st.success("✅ مربی در ابرها بیدار شد! بات لپ‌تاپ را خاموش کن.")
