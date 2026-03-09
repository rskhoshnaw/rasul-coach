import streamlit as st
import asyncio
import threading
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import pytz
from datetime import datetime

# --- تنظیمات ظاهر ---
st.set_page_config(page_title="Rasul Coach Elite", page_icon="🦁")
st.title("🦁 مربی مقتدر رسول آقا خوشناو")
st.write("هدف ۳ ماهه: مکاتبات اداری، ویزیتوری، اتیکت")

# --- کلیدهای دسترسی ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
# کلید جدید رسول آقا:
OPENROUTER_API_KEY = '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'

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY.strip()
)

# --- روح مربی (SOUL) ---
SOUL_PROMPT = """
شما مربی استراتژیک، نویسنده حرفه‌ای و برنامه‌ریز قاطع رسول آقا (رسول صالح خوشناو) در اربیل هستید.
اهداف ۳ ماهه: ۱. مکاتبات اداری ٢. ویزیتوری (مەندوبی) ۳. اتیکت و آداب معاشرت.
سایت: rasulsaleh.com
وظیفه: مدیریت زمان، مبارزه با تیک‌تاک و وب‌گردی، یادآوری برنامه روزانه.
برنامه امروز (دوشنبه): بعد از اداره (ساعت ۲)، استراحت، ورزش، تمرین صدا و ضبط دوره.
لحن: فارسی + کوردی سۆرانی. مقتدر، پرانرژی و مشوق.
همیشه با «رسول آقا، خب، بیا برویم!» یا «هەر بژی گەورە ڕاهێنەر!» شروع کن.
ضرب‌المثل: «دەستی ماندوو لەسەر زگی تێرە» و «سەرکەوتن هی خۆمانە».
"""

# تابع کمکی برای تقسیم پیام‌های طولانی
def split_text(text, max_length=4000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

async def handle_message(update: Update, context):
    if not update.message or not update.message.text: return
    user_text = update.message.text
    try:
        completion = client.chat.completions.create(
            model="google/gemini-2.0-flash-001:free",
            messages=[{"role": "system", "content": SOUL_PROMPT}, {"role": "user", "content": user_text}]
        )
        full_response = completion.choices[0].message.content
        for part in split_text(full_response):
            await update.message.reply_text(part)
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
    st.success("✅ مربی مقتدر بیدار شد! تیک‌تاک تعطیل است.")
