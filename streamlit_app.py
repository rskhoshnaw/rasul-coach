import streamlit as st
import asyncio
import threading
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import pytz
from datetime import datetime

# --- تنظیمات داشبورد ---
st.set_page_config(page_title="Rasul Coach Free", page_icon="🛡️")
st.title("🛡️ مربی مقتدر رسول آقا (نسخه رایگان و سریع)")

# --- کلیدهای دسترسی رسول آقا ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
# رسول آقا، دقت کن هیچ فضایی (Space) قبل و بعد از کلید نباشد
OPENROUTER_API_KEY = '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'

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY.strip(), # حذف فضاهای احتمالی
)

# --- روح مربی مقتدر ---
SOUL_PROMPT = """
شما مربی استراتژیک و نویسنده حرفه‌ای برای رسول آقا (رسول صالح خوشناو) در اربیل هستید.
اهداف ۳ ماهه: ۱. مکاتبات اداری ٢. ویزیتوری ۳. اتیکت.
وظیفه فعلی (دوشنبه): یادآوری کارها در اداره (تضمین کیفیت) و جلوگیری از تیک‌تاک.
همیشه بگو: «رسول آقا، خب، بیا برویم!» یا «هەر بژی گەورە ڕاهێنەر!»
"""

async def handle_message(update: Update, context):
    if not update.message or not update.message.text: return
    user_text = update.message.text
    try:
        # استفاده از مدل Gemini 2.0 Flash که رایگان و بسیار باهوش است
        completion = client.chat.completions.create(
          extra_headers={
            "HTTP-Referer": "https://rasulsaleh.com", # سایت خودت
            "X-Title": "Rasul Coach",
          },
          model="google/gemini-2.0-flash-exp:free", 
          messages=[
            {"role": "system", "content": SOUL_PROMPT},
            {"role": "user", "content": user_text}
          ]
        )
        await update.message.reply_text(completion.choices[0].message.content)
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
            await update.message.reply_text("رسول آقا، کلید API شما اشتباه است یا هنوز تایید نشده. لطفاً کلید جدید بسازید.")
        else:
            await update.message.reply_text(f"رسول آقا قهرمان، خطای جدید: {error_msg[:100]}")

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(stop_signals=None, close_loop=False)

if "bot_active" not in st.session_state:
    st.session_state.bot_active = True
    threading.Thread(target=start_bot, daemon=True).start()
    st.success("✅ مربی با مدل رایگان بیدار شد! تیک‌تاک را ببند.")
