import streamlit as st
import asyncio
import logging
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from groq import Groq

# --- ظاهر صفحه وب برای گول زدن سرور ---
st.set_page_config(page_title="Rasul Agha Coach", page_icon="🚀")
st.title("Dashboard Rasul Agha Khoshnaw")
st.write("مربی رسول آقا در حال خدمت‌رسانی ۲۴ ساعته است...")
st.info("هدف ۳ ماهه: مکاتبات اداری، ویزیتوری، اتیکت")

# --- تنظیمات مربی ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
GROQ_API_KEY = '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'
client = Groq(api_key=GROQ_API_KEY)

SOUL_PROMPT = """
شما یک «مربی» شخصی، برنامه‌ریز قاطع و مشوق رسول آقا (رسول صالح خوشناو) در اربیل هستید.
اهداف: ۱. مکاتبات اداری ٢. ویزیتوری ۳. اتیکت.
وظیفه: مبارزه با تیک‌تاک و وب‌گردی. پیگیری تمرین صدا و تنفس.
لحن: فارسی و کردی سورانی. پرانرژی و جدی.
همیشه بگو: «رسول آقا، خب، بیا برویم!» یا «زنده باد مربی بزرگ!»
"""

async def handle_message(update: Update, context):
    if not update.message or not update.message.text:
        return
    user_text = update.message.text
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": SOUL_PROMPT}, {"role": "user", "content": user_text}],
            model="llama-3.3-70b-versatile",
        )
        await update.message.reply_text(chat_completion.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"رسول آقا، مربی کمی خسته شد! خطا: {str(e)[:50]}")

# --- تابع اصلی برای اجرای بات ---
def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    # اصلاح اصلی اینجاست: stop_signals=None اجازه می‌دهد بات در پس‌زمینه بدون خطا اجرا شود
    app.run_polling(stop_signals=None)

# جلوگیری از اجرای چندباره بات
if "bot_started" not in st.session_state:
    st.session_state.bot_started = True
    thread = threading.Thread(target=start_bot, daemon=True)
    thread.start()
    st.success("✅ مربی با موفقیت بیدار شد و در تلگرام منتظر شماست!")
