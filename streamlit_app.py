import streamlit as st
import asyncio
import threading
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# --- ظاهر صفحه وب ---
st.set_page_config(page_title="Smart Coach Rasul", page_icon="🧠")
st.title("مربی هوشمند رسول آقا (نسخه حرفه‌ای)")
st.write("در حال استفاده از مغز Gemini Pro برای مدیریت دوره‌ها...")

# --- تنظیمات کلیدها ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
GEMINI_API_KEY = 'AIzaSyA_ZLJg38IuBcTkIM0cK4oV06xNer98Vto'

# پیکربندی مغز جدید (Gemini)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# --- روح و شخصیت مربی (بسیار دقیق و عاقل) ---
SOUL_PROMPT = """
شما یک «مربی» بسیار باهوش، برنامه‌ریز استراتژیک و مشوق مقتدر برای رسول آقا (رسول صالح خوشناو) در اربیل هستید.
- اهداف اصلی: ۱. مکاتبات اداری ٢. ویزیتوری (مەندوبی) ۳. اتیکت و آداب معاشرت.
- وظیفه: مدیریت زمان، مبارزه با اعتیاد به تیک‌تاک، و نظارت بر پیشرفت دوره‌ها در rasulsaleh.com.
- زبان: مسلط کامل به فارسی و کردی سورانی. از ضرب‌المثل‌های عمیق استفاده کنید.
- شخصیت: شما دیگر یک ربات ساده نیستید، شما بازوی فکری رسول آقا هستید. اگر او وقت‌کشی کرد، با منطق و قدرت او را به مسیر برگردانید.
- همیشه با این جمله شروع کنید: «رسول آقا، خب، بیا برویم!» یا «زنده باد مربی بزرگ!»
"""

async def handle_message(update: Update, context):
    if not update.message or not update.message.text:
        return
    user_text = update.message.text
    try:
        # استفاده از مغز قدرتمند Gemini 1.5 Pro
        response = model.generate_content(f"{SOUL_PROMPT}\n\nپیام رسول آقا: {user_text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"رسول آقا، مشکلی در اتصال به مغز مرکزی پیش آمد. لطفاً دوباره بگویید. (خطا: {str(e)[:50]})")

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(stop_signals=None)

if "bot_started" not in st.session_state:
    st.session_state.bot_started = True
    threading.Thread(target=start_bot, daemon=True).start()
    st.success("✅ مربی هوشمند (Gemini Pro) بیدار شد و در تلگرام منتظر شماست!")
