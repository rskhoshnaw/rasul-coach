import streamlit as st
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from groq import Groq

# --- ظاهر صفحه وب برای گول زدن سرور ---
st.title("Dashboard Rasul Agha")
st.write("مربی رسول آقا در حال خدمت‌رسانی است...")

# --- تنظیمات مربی ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
GROQ_API_KEY = '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'
client = Groq(api_key=GROQ_API_KEY)

SOUL_PROMPT = "شما مربی قاطع رسول آقا در اربیل هستید. هدف: مکاتبات اداری، ویزیتوری و اتیکت. نگذار وقتش در تیک تاک تلف شود. همیشه بگو: رسول آقا، خب، بیا برویم!"

async def handle_message(update: Update, context):
    user_text = update.message.text
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": SOUL_PROMPT}, {"role": "user", "content": user_text}],
            model="llama-3.3-70b-versatile",
        )
        await update.message.reply_text(chat_completion.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"خطا: {str(e)[:50]}")

# --- راه اندازی بات در پس‌زمینه ---
if "bot_started" not in st.session_state:
    st.session_state.bot_started = True
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    # اجرای بات بدون بلاک کردن صفحه وب
    import threading
    def run_bot():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        app.run_polling()
    
    threading.Thread(target=run_bot, daemon=True).start()
    st.success("مربی با موفقیت بیدار شد!")