import streamlit as st
import asyncio
import threading
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import pytz
from datetime import datetime

# --- تنظیمات داشبورد ---
st.set_page_config(page_title="Rasul Coach Elite", page_icon="🏆")
st.title("🏆 مربی مقتدر رسول آقا خوشناو")
st.write("سیستم مدیریت اهداف ۳ ماهه: فعال")

# --- کدهای دسترسی ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
GEMINI_API_KEY = 'AIzaSyA_ZLJg38IuBcTkIM0cK4oV06xNer98Vto'

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- روح و شخصیت مربی (بسیار هوشمند و قاطع) ---
SOUL_PROMPT = """
تۆ «مربی»یت، مربی شخصی، نویسنده استراتژیک و مشوق رسول آقا (رسول صالح خوشناو) لە هەولێر.
اهداف: آمادە‌سازی و بازریابی و فروش دوره مکاتبات اداری و فروش دوره در rasulsaleh.com.
وظیفه: نگذار وقت رسول آقا در تیک‌تاک تلف شود.
برنامه امروز دوشنبه: تا ساعت ۲ بعدازظهر در اداره (تضمین کیفیت) هستی. بعد از آن ورزش، تمرین صدا و ضبط دوره.
لحن: فارسی + کوردی سۆرانی. مقتدر و پرانرژی.
همیشه با «رسول آقا، خب، بیا برویم!» یا «هەر بژی گەورە ڕاهێنەر!» شروع کن.
"""

async def handle_message(update: Update, context):
    if not update.message or not update.message.text: return
    user_text = update.message.text
    try:
        # مغز مربی
        response = model.generate_content(f"{SOUL_PROMPT}\n\nرسول آقا می‌گوید: {user_text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"رسول آقا، مشکلی در مغز گوگل رخ داد. دوباره بگو! (خطا: {str(e)[:50]})")

def start_bot():
    # اصلاح تداخل پایتون ۳.۱۴
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    # اجرای بات به شکلی که در سرور کرش نکند
    app.run_polling(close_loop=False, stop_signals=None)

# جلوگیری از اجرای چندباره
if "bot_running" not in st.session_state:
    st.session_state.bot_running = True
    threading.Thread(target=start_bot, daemon=True).start()
    st.success("✅ مربی رسول آقا بیدار شد و آماده نبرد است!")
