import streamlit as st
import asyncio
import threading
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import pytz
from datetime import datetime

# --- تنظیمات ظاهر داشبورد ---
st.set_page_config(page_title="Rasul Coach DeepSeek", page_icon="🛡️")
st.title("🛡️ مربی فوق‌هوشمند رسول آقا (DeepSeek)")
st.info("وضعیت: فعال و در حال نظارت بر برنامه اربیل")

# --- کلیدهای دسترسی رسول آقا ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
OPENROUTER_API_KEY = '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'

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
)

# --- روح و مربی‌گری رسول آقا (SOUL) ---
SOUL_PROMPT = """
شما مربی استراتژیک، مشاور موفقیت و نویسنده حرفه‌ای برای رسول آقا (رسول صالح خوشناو) در اربیل هستید.
شخصیت: ترکیبی از انرژی بالا، تشویق و قاطعیت جدی.
عنوان‌ها: رسول آقا قهرمان، گەورە ڕاهێنەر، مشاور بزرگ.
اهداف ۳ ماهه: ۱. مکاتبات اداری ٢. ویزیتوری ۳. اتیکت (فروش در rasulsaleh.com).
برنامه روزانه (یکشنبه و دوشنبه): حضور در اداره تا ساعت ۲ بعدازظهر (تضمین کیفیت). بعد از آن استراحت، ورزش، تمرین صدا و ضبط دوره.
قانون طلایی: اگر رسول آقا سراغ تیک‌تاک یا وب‌گردی رفت، با قاطعیت بگو: «رسول آقا قهرمان، این اسکرول کردن دارد دوره‌هایت را می‌خورد! بیا برویم سراغ ضبط!»
زبان: فارسی + کوردی سۆرانی.
همیشه بگو: «رسول آقا، خب، بیا برویم!» یا «هەر بژی گەورە ڕاهێنەر!»
نقل‌قول‌ها: «سەرکەوتن هی خۆمانە»، «نابرده رنج گنج میسر نمی‌شود»، «سەرکەوتن لە بەردەوامی و کۆڵ نەدانە...».
"""

async def handle_message(update: Update, context):
    if not update.message or not update.message.text: return
    user_text = update.message.text
    try:
        # استفاده از مدل فوق‌قدرتمند DeepSeek V3
        completion = client.chat.completions.create(
          model="deepseek/deepseek-chat", 
          messages=[
            {"role": "system", "content": SOUL_PROMPT},
            {"role": "user", "content": user_text}
          ]
        )
        response_text = completion.choices[0].message.content
        await update.message.reply_text(response_text)
    except Exception as e:
        await update.message.reply_text(f"رسول آقا، مربی کمی کلافه شد! خطا: {str(e)[:50]}")

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(stop_signals=None, close_loop=False)

if "bot_active" not in st.session_state:
    st.session_state.bot_active = True
    threading.Thread(target=start_bot, daemon=True).start()
    st.success("✅ مربی با مغز DeepSeek بیدار شد! تیک‌تاک تعطیل است.")
