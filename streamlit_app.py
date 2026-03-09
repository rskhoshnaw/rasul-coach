import streamlit as st
import asyncio
import threading
import os

# تلاش برای وارد کردن کتابخانه؛ اگر نبود، خطای واضح بدهد
try:
    from openai import OpenAI
except ImportError:
    st.error("کتابخانه openai نصب نشده است. لطفا فایل requirements.txt را چک کنید.")

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# --- ظاهر داشبورد رسول آقا ---
st.set_page_config(page_title="Rasul Coach Ultra", page_icon="🛡️")
st.title("🛡️ مربی مقتدر رسول آقا (DeepSeek)")
st.write("هدف: مکاتبات اداری، ویزیتوری و اتیکت در rasulsaleh.com")

# --- کلیدهای دسترسی ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
OPENROUTER_API_KEY = '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'

# --- تنظیمات مربی (SOUL) ---
SOUL_PROMPT = """
شما مربی استراتژیک، مشاور موفقیت و نویسنده حرفه‌ای برای رسول آقا (رسول صالح خوشناو) در اربیل هستید.
اهداف: مکاتبات اداری، ویزیتوری/مەندوبی، اتیکت.
وظیفه: نگذار وقت رسول آقا در تیک‌تاک تلف شود. رسول آقا الان از اداره برگشته و باید ضبط دوره را شروع کند.
همیشه بگو: «رسول آقا، خب، بیا برویم!» یا «هەر بژی گەورە ڕاهێنەر!»
ضرب‌المثل: «سەرکەوتن لە بەردەوامی و کۆڵ نەدانە...»
"""

async def handle_message(update: Update, context):
    if not update.message or not update.message.text: return
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
        
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": SOUL_PROMPT},
                {"role": "user", "content": update.message.text}
            ]
        )
        await update.message.reply_text(completion.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"رسول آقا، مشکلی پیش آمد: {str(e)[:100]}")

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(stop_signals=None, close_loop=False)

if "bot_active" not in st.session_state:
    st.session_state.bot_active = True
    threading.Thread(target=start_bot, daemon=True).start()
    st.success("✅ مربی مقتدر (DeepSeek) بیدار شد! تیک‌تاک تعطیل است.")
