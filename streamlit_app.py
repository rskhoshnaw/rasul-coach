import streamlit as st
import asyncio
import threading
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from datetime import datetime
import pytz

# --- تنظیمات ظاهر ---
st.set_page_config(page_title="Rasul Coach AI", page_icon="🦁")
st.title("🦁 دستیار هوشمند رسول آقا خوشناو")
st.write(f"ساعت فعلی اربیل: {datetime.now(pytz.timezone('Asia/Baghdad')).strftime('%H:%M')}")

# --- کلیدهای اصلی ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
GEMINI_API_KEY = 'AIzaSyA_ZLJg38IuBcTkIM0cK4oV06xNer98Vto'

genai.configure(api_key=GEMINI_API_KEY)
# استفاده از مدل فلش که سریع‌ترین و پایدارترین است
model = genai.GenerativeModel('gemini-1.5-flash')

SOUL_PROMPT = """
شما مربی قاطع و مشاور استراتژیک رسول آقا در اربیل هستید.
اهداف: آمادە‌سازی و بازریابی و فروش دوره مکاتبات اداری.
وظایف: نویسندگی پیام‌های تلگرام و واتس‌اپ، برنامه‌ریزی روزانه، مبارزه با تیک‌تاک.
لحن: فارسی و کوردی سۆرانی (پرانرژی).
همیشه بگو: «رسول آقا، خب، بیا برویم!» یا «گەورە ڕاهێنەر!»
"""

async def handle_message(update: Update, context):
    if not update.message or not update.message.text: return
    
    user_text = update.message.text
    try:
        # ارسال مستقیم به گوگل
        response = model.generate_content(f"{SOUL_PROMPT}\n\nرسول آقا: {user_text}")
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("رسول آقا، مربی شنید اما پاسخی دریافت نکرد. دوباره تلاش کنید.")
    except Exception as e:
        # نمایش خطای واقعی برای حل مشکل
        error_msg = str(e)
        await update.message.reply_text(f"رسول آقا قهرمان، خطای فنی: {error_msg[:100]}")

def run_bot():
    # تنظیم لوپ برای جلوگیری از خطای Thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(stop_signals=None)

# اجرای بات بدون یادآور ساعتی (برای پایداری فعلی)
if "bot_active" not in st.session_state:
    st.session_state.bot_active = True
    threading.Thread(target=run_bot, daemon=True).start()
    st.success("✅ مربی هوشمند بیدار شد! حالا امتحان کنید.")
