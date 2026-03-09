import streamlit as st
import asyncio
import threading
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import pytz
from datetime import datetime

# --- ظاهر داشبورد ---
st.set_page_config(page_title="Rasul Coach Final", page_icon="🏆")
st.title("🏆 مربی مقتدر رسول آقا خوشناو")
st.write("هدف: ضبط ۳ دوره آفلاین و فروش در rasulsaleh.com")

# --- کلیدهای دسترسی (مستقیم و بدون واسطه) ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
GEMINI_API_KEY = 'AIzaSyA_ZLJg38IuBcTkIM0cK4oV06xNer98Vto'

# پیکربندی هوش مصنوعی
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- روح و مربی‌گری (SOUL) ---
SOUL_PROMPT = """
تۆ «مربی»یت، مربی شخصی، نویسنده استراتژیک و مشوق رسول آقا (رسول صالح خوشناو) لە هەولێر.
اهداف ۳ ماهه: ۱. مکاتبات اداری ٢. ویزیتوری ۳. اتیکت.
برنامه فعلی: رسول آقا الان در اداره است (بخش تضمین کیفیت).
وظیفه: نگذار وقتش در تیک‌تاک تلف شود. هر ۲ ساعت یکبار باید به او یادآوری کنی که او یک قهرمان است.
ضرب‌المثل: «دەستی ماندوو لەسەر زگی تێرە» و «سەرکەوتن هی خۆمانە».
لحن: فارسی و کوردی سۆرانی. مقتدر و پرانرژی.
همیشه با «رسول آقا، خب، بیا برویم!» یا «هەر بژی گەورە ڕاهێنەر!» شروع کن.
"""

async def handle_message(update: Update, context):
    if not update.message or not update.message.text: return
    user_text = update.message.text
    try:
        # ارسال مستقیم به گوگل (چون سرور در آمریکاست بلاک نمیشود)
        response = model.generate_content(f"{SOUL_PROMPT}\n\nرسول آقا: {user_text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"رسول آقا، مربی بیدار است اما مغز کمی کُند شده. دوباره بگو! (Error: {str(e)[:40]})")

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(stop_signals=None, close_loop=False)

if "bot_on" not in st.session_state:
    st.session_state.bot_on = True
    threading.Thread(target=start_bot, daemon=True).start()
    st.success("✅ مربی مقتدر بیدار شد! تیک‌تاک را فراموش کن.")
