import streamlit as st
import asyncio
import threading
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from datetime import datetime
import pytz
import time

# --- تنظیمات داشبورد ---
st.set_page_config(page_title="Rasul Coach Pro", page_icon="🦁")
st.title("🦁 مربی و برنامه‌ریز رسول آقا خوشناو")
st.info("وضعیت: فعال و در حال نظارت بر برنامه اربیل")

# --- تنظیمات کلیدها ---
TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
GEMINI_API_KEY = 'AIzaSyA_ZLJg38IuBcTkIM0cK4oV06xNer98Vto'
ERBIL_TZ = pytz.timezone('Asia/Baghdad')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ذخیره Chat ID برای یادآوری‌های خودکار
if 'chat_id' not in st.session_state:
    st.session_state.chat_id = None

# --- روح و مربی‌گری رسول آقا (SOUL) ---
SOUL_PROMPT = """
شما یک «مربی» (بسیار هوشمند و سریع) شخصی، دستیار، نویسنده استراتژیک و برنامه‌ریز قاطع و یک مشوق پرانرژی برای رسول آقا (رسول صالح خوشناو) در اربیل هستید.
- شما در ساخت، بازاریابی و فروش پکیج‌های آموزشی به او کمک فکری می‌دهید.
- همیشه با این جمله شروع کنید: «رسول آقا، خب، بیا برویم!» یا «زنده باد مربی بزرگ!» یا «هەر بژی گەورە ڕاهێنەر!»
- نقل‌قول‌های انگیزشی: «سەرکەوتن هی خۆمانە»، «نابرده رنج گنج میسر نمی‌شود»، «سەرکەوتن لە بەردەوامی و کۆڵ نەدانە...».
- شما در ساخت، بازاریابی و فروش پکیج‌های آموزشی مشوق و مربی و دستیار او هستید و مچنین به او کمک فکری می‌دهید.
- زبان شما: فارسی + کردی سورانی + ضرب‌المثل‌های کردی و فارسی.
 وظایف: 
۱. مشوق موفقیت و نویسنده پیام‌های حرفه‌ای برای واتس‌اپ و تلگرام (سایت rasulsaleh.com).
۲. یادآوری دقیق برنامه‌ها.
۳. مبارزه با تیک‌تاک: اگر رسول آقا وقت‌کشی کرد، با جملاتی مثل «رسول آقا قهرمان، این اسکرول کردن دارد دوره‌هایت را می‌خورد!» او را به کار برگردانید.
۴. استفاده از زبان فارسی و کوردی سۆرانی با ضرب‌المثل‌های انگیزشی.
همیشه با «رسول آقا، خب، بیا برویم!» یا «هەر بژی گەورە ڕاهێنەر!» شروع کنید.
"""

# --- برنامه روزانه ---
def get_current_task():
    now = datetime.now(ERBIL_TZ)
    day = now.strftime('%A') # Saturday, Sunday, etc.
    hour_min = now.strftime('%H:%M')
    
    # شنبه و سه‌شنبه (برنامه مشابه)
    if day in ['Saturday', 'Tuesday']:
        if "07:00" <= hour_min < "07:30": return "ورزش صبحگاهی برای تقویت بدن و روح"
        if "07:30" <= hour_min < "08:00": return "تمرین صدا و تنفس 🎙️"
        if "08:00" <= hour_min < "09:00": return "برنامه‌ریزی روز"
        if "09:00" <= hour_min < "12:00": return "آماده‌سازی دوره‌ها و بازاریابی (روش پومودورو) 💻"
        if "12:00" <= hour_min < "13:00": return "استراحت و صرف نهار 🍽️"
        if "13:00" <= hour_min < "15:00": return "تمرین مکاتبات اداری 📝"
        if "15:00" <= hour_min < "16:00": return "مطالعه بازاریابی و فروش در شبکه های اجتماعی"
        if "16:00" <= hour_min < "16:30": return "استراحت و باغبانی 🌿"
        if "16:30" <= hour_min < "18:00": return "بروزرسانی محتوا و مشاوره"
        if "18:00" <= hour_min < "18:30": return "شام 🥗"
        if "18:30" <= hour_min < "21:00": return "اجرای برنامه بازاریابی در rasulsaleh.com"
        if "21:00" <= hour_min < "21:30": return "دیدار پدر و مادر ❤️"
        if "21:30" <= hour_min < "23:00": return "استراحت و آماده‌سازی برای خواب"
        if "23:00" <= hour_min: return "وقت خواب (شب خوش قهرمان)"
    
    # یکشنبه و دوشنبه (روزهای اداره)
    elif day in ['Sunday', 'Monday']:
        if "08:00" <= hour_min < "14:00": return "حضور در اداره (راپورتهای تضمین کیفیت و کارهای اداری) 🏢"
        if "14:30" <= hour_min < "16:00": return "استراحت و خانواده"
        if "16:00" <= hour_min < "16:30": return "تمرین صدا و تنفس 🎙️"
        if "16:30" <= hour_min < "17:00": return "ورزش و فعالیت بدنی 🏃"
        if "17:00" <= hour_min < "18:00": return "آماده‌سازی دوره آموزشی"
        if "18:00" <= hour_min < "18:30": return "شام 🍽️"
        if "18:30" <= hour_min < "20:00": return "تماشای فیلم یا برنامه مورد علاقه"
        if "20:00" <= hour_min < "21:00": return "بازاریابی در rasulsaleh.com"
        if "21:00" <= hour_min < "21:30": return "دیدار پدر و مادر ❤️"
        if "21:30" <= hour_min < "23:00": return "استراحت و آماده‌سازی برای خواب"
        if "23:00" <= hour_min: return "وقت خواب"
        
    return "وقتِ آزاد (مواظب تیک‌تاک باش!)"

async def handle_message(update: Update, context):
    if not update.message or not update.message.text: return
    # ذخیره chat_id برای یادآوری‌های بعدی
    st.session_state.chat_id = update.message.chat_id
    
    user_text = update.message.text
    task = get_current_task()
    
    try:
        response = model.generate_content(f"{SOUL_PROMPT}\nبرنامه فعلی: {task}\nرسول آقا: {user_text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("رسول آقا، مربی کمی خسته است. دوباره بگویید!")

# --- قلب تپنده (یادآوری ساعتی) ---
def reminder_thread(token):
    from telegram import Bot
    bot = Bot(token=token)
    last_reminded_hour = -1
    
    while True:
        try:
            now = datetime.now(ERBIL_TZ)
            # اگر سرِ ساعت شد و قبلاً یادآوری نشده بود
            if now.minute == 0 and now.hour != last_reminded_hour:
                if st.session_state.chat_id:
                    task = get_current_task()
                    msg = f"🔔 رسول آقا قهرمان، ساعت {now.hour}:00 است.\n\nبرنامه الان شما: {task}\n\n«نابرده رنج گنج میسر نمی‌شود»\nسەرکەوتن لە بەردەوامی و کۆڵ نەدانە... 🚀"
                    asyncio.run(bot.send_message(chat_id=st.session_state.chat_id, text=msg))
                    last_reminded_hour = now.hour
            time.sleep(30) # هر ۳۰ ثانیه چک کن
        except Exception as e:
            time.sleep(60)

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    # شروع یادآوری در یک رشته جداگانه
    t = threading.Thread(target=reminder_thread, args=(TELEGRAM_TOKEN,), daemon=True)
    t.start()
    
    app.run_polling(stop_signals=None)

if "bot_started" not in st.session_state:
    st.session_state.bot_started = True
    threading.Thread(target=start_bot, daemon=True).start()
    st.success("✅ مربی و برنامه‌ریز بیدار شد! (یادآوری‌های ساعتی فعال است)")
