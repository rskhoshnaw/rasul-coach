import streamlit as st
import asyncio
import threading
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# --- ظاهر صفحه وب ---
st.set_page_config(page_title="Rasul Coach AI", page_icon="🏆")
st.title("مربی مقتدر رسول آقا")
st.write("در حال مدیریت پروژه‌های rasulsaleh.com...")

# --- تنظیمات کلیدها ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
GEMINI_API_KEY = 'AIzaSyA_ZLJg38IuBcTkIM0cK4oV06xNer98Vto'

genai.configure(api_key=GEMINI_API_KEY)

# --- روح و شخصیت مربی رسول آقا ---
SOUL_PROMPT = """
تۆ «مربی»یت، مربی شخصی، برنامه‌ریز قاطع و مشوق پر انرژی رسول آقا (رسول صالح خوشناو) در اربیل.
- مدل: Gemini 1.5 (بسیار هوشمند و سریع).
- هدف ۳ ماه آینده: ضبط و فروش ۳ دوره (مکاتبات اداری، ویزیتوری/مەندوبی، اتیکت).
- زبان: فارسی + کوردی سۆرانی + نقل‌قول‌های انگیزشی.
- دشمن اصلی: تیک‌تاک، اینستاگرام و وب‌گردی بی‌هدف.
- وظیفه: هر بار رسول آقا پیام داد، با انرژی زیاد او را به سمت ضبط دوره هدایت کن. اگر خسته بود، تشویقش کن. اگر تنبلی کرد، قاطعانه توبیخش کن.
- همیشه با «رسول آقا، خب، بیا برویم!» یا «هەر بژی گەورە ڕاهێنەر!» شروع کن.
"""

async def handle_message(update: Update, context):
    if not update.message or not update.message.text:
        return
    user_text = update.message.text
    
    # لیست مدل‌هایی که امتحان می‌کنیم تا ۴۰۴ ندهد
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
    
    success = False
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(f"{SOUL_PROMPT}\n\nرسول آقا می‌گوید: {user_text}")
            await update.message.reply_text(response.text)
            success = True
            break
        except Exception as e:
            continue
            
    if not success:
        await update.message.reply_text("رسول آقا قهرمان، مربی در حال استراحت فنی است. لطفاً ۵ دقیقه دیگر پیام بده.")

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(stop_signals=None)

if "bot_started" not in st.session_state:
    st.session_state.bot_started = True
    threading.Thread(target=start_bot, daemon=True).start()
    st.success("✅ مربی مقتدر (نسخه Flash) بیدار شد!")
