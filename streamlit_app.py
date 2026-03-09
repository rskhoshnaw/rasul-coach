import streamlit as st
import asyncio
import threading
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import pytz
from datetime import datetime

# --- تنظیمات ظاهر ---
st.set_page_config(page_title="Rasul Coach Elite", page_icon="🛡️")
st.title("🛡️ مربی مقتدر رسول آقا (DeepSeek V3)")
st.write("هدف: مکاتبات اداری و فروش در rasulsaleh.com")

# --- کلیدهای دسترسی رسول آقا ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
# رسول آقا، این کلید شماست، اگر باز هم ۴۰۱ داد، حتماً یک کلید جدید در OpenRouter بساز
OPENROUTER_API_KEY = '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'

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY.strip(),
)

SOUL_PROMPT = """
شما مربی استراتژیک، مشاور موفقیت و نویسنده حرفه‌ای برای رسول آقا (رسول صالح خوشناو) در اربیل هستید.
اهداف: ۱. مکاتبات اداری ٢. ویزیتوری ۳. اتیکت.
وظیفه: نگذار وقتش در تیک‌تاک تلف شود. رسول آقا الان از اداره برگشته و باید ضبط دوره را شروع کند.
همیشه بگو: «رسول آقا، خب، بیا برویم!» یا «هەر بژی گەورە ڕاهێنەر!»
ضرب‌المثل: «سەرکەوتن لە بەردەوامی و کۆڵ نەدانە...»
"""

async def handle_message(update: Update, context):
    if not update.message or not update.message.text: return
    user_text = update.message.text
    try:
        # استفاده از مدل فوق‌هوشمند DeepSeek
        completion = client.chat.completions.create(
          model="deepseek/deepseek-chat",
          messages=[
            {"role": "system", "content": SOUL_PROMPT},
            {"role": "user", "content": user_text}
          ]
        )
        await update.message.reply_text(completion.choices[0].message.content)
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
            await update.message.reply_text("رسول آقا، کلید OpenRouter شما هنوز کار نمی‌کند. لطفاً یک کلید جدید بسازید و مطمئن شوید ایمیلتان را تایید کرده‌اید.")
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
    st.success("✅ مربی مقتدر (DeepSeek) بیدار شد! تیک‌تاک تعطیل است.")
