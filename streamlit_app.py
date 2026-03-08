import streamlit as st
import asyncio
import threading
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# --- ظاهر صفحه وب برای رسول آقا ---
st.set_page_config(page_title="Rasul Coach AI", page_icon="🦁")
st.title("🦁 مربی مقتدر رسول آقا")
st.write("هدف ۳ ماهه: ضبط دوره‌های مکاتبات، ویزیتوری و اتیکت")

# --- تنظیمات کلیدها ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
GEMINI_API_KEY = 'AIzaSyA_ZLJg38IuBcTkIM0cK4oV06xNer98Vto'

# تنظیم مغز گوگل
genai.configure(api_key=GEMINI_API_KEY)

# --- روح و شخصیت مربی رسول آقا ---
SOUL_PROMPT = """
تۆ «مربی»یت، مربی شخصی، برنامه‌ریز قاطع و مشوق رسول آقا (رسول صالح خوشناو) لە هەولێر.
- هدف: ضبط و فروش دوره‌های (مکاتبات اداری، ویزیتوری/مەندوبی، اتیکت).
- زبان: فارسی + کوردی سۆرانی.
- وظیفه: نگذار وقت رسول آقا در تیک‌تاک و اینستاگرام تلف شود.
- همیشه با «رسول آقا، خب، بیا برویم!» یا «هەر بژی گەورە ڕاهێنەر!» شروع کن.
"""

async def handle_message(update: Update, context):
    if not update.message or not update.message.text: return
    user_text = update.message.text
    
    try:
        # استفاده مستقیم از مدل لیتست (Latest)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(f"{SOUL_PROMPT}\n\nرسول آقا می‌گوید: {user_text}")
        
        if response and response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("رسول آقا قهرمان، مربی شنید، ولی گوگل جوابی نداد. دوباره بگو!")
            
    except Exception as e:
        error_msg = str(e)
        # نمایش خطای دقیق در تلگرام برای پیدا کردن مشکل
        await update.message.reply_text(f"رسول آقا، خطای مغزی: {error_msg[:100]}")

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # اضافه کردن پاردامترهای ضدِ تداخل (Conflict)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(stop_signals=None)

if "bot_started" not in st.session_state:
    st.session_state.bot_started = True
    threading.Thread(target=start_bot, daemon=True).start()
    st.success("✅ مربی مقتدر بیدار شد!")
