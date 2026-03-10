import streamlit as st
import google.generativeai as genai
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update
import threading
import time
from datetime import datetime
import pytz
import random

# --------- Secrets ---------

TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
GEMINI_KEY = st.secrets["GEMINI_KEY"]

# --------- Gemini ---------

genai.configure(api_key=GEMINI_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# --------- Timezone ---------

tz = pytz.timezone("Asia/Baghdad")

# --------- User data ---------

chat_id = None
last_user_message = time.time()

# --------- Coach personality ---------

SYSTEM_PROMPT = """
تو مربی شخصی رسول صالح خوشناو هستی.

نام او: رسول آقا

لحن:
فارسی + کوردی سورانی
انرژی بالا
قاطع و مشوق

تکیه کلام:
رسول آقا، خب، بیا برویم!
سەرکەوتن هی خۆمانە

هدف‌ها:

ضبط دوره مکاتبات اداری
ضبط دوره ویزیتوری
ضبط دوره اتیکت

کار تو:
تشویق کردن
جلوگیری از اتلاف وقت
کمک به بازاریابی سایت rasulsaleh.com
"""

# --------- Schedule ---------

schedule = {

"Saturday":[
("07:00","وقت ورزش"),
("07:30","تمرین صدا"),
("08:00","برنامه ریزی روز"),
("09:00","ساخت دوره"),
("13:00","مکاتبات اداری"),
("18:30","بازاریابی سایت"),
("21:00","دیدار والدین")
],

"Tuesday":[
("07:00","ورزش"),
("07:30","تمرین صدا"),
("08:00","برنامه ریزی"),
("09:00","ساخت دوره"),
("13:00","مکاتبات اداری"),
("18:30","بازاریابی سایت"),
("21:00","دیدار والدین")
],

"Sunday":[
("08:00","رفتن به اداره"),
("10:00","تمرکز روی کار"),
("12:00","ادامه کار"),
("16:00","تمرین صدا"),
("17:00","ساخت دوره"),
("20:00","بازاریابی سایت"),
("21:00","دیدار والدین")
],

"Monday":[
("08:00","رفتن به اداره"),
("10:00","تمرکز"),
("12:00","ادامه کار"),
("16:00","تمرین صدا"),
("17:00","ساخت دوره"),
("20:00","بازاریابی سایت"),
("21:00","دیدار والدین")
]

}

motivation = [
"رسول آقا تمرکز!",
"سەرکەوتن هی خۆمانە",
"یک ساعت کار = یک قدم موفقیت",
"رسول آقا خب بیا برویم",
"امروز آینده ساخته می‌شود"
]

# --------- Telegram message handler ---------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global chat_id, last_user_message

    chat_id = update.effective_chat.id
    user_text = update.message.text

    last_user_message = time.time()

    prompt = SYSTEM_PROMPT + "\nUser:" + user_text

    try:

        response = model.generate_content(prompt)

        reply = response.text

    except Exception as e:

        reply = f"""
رسول آقا ⚠️

مشکل در ارتباط با هوش مصنوعی

{str(e)}
"""

    await update.message.reply_text(reply)

# --------- Reminder system ---------

def reminder_loop(bot):

    last_sent=""

    while True:

        now=datetime.now(tz)

        day=now.strftime("%A")
        current=now.strftime("%H:%M")

        if day in schedule:

            for t,task in schedule[day]:

                if current==t and last_sent!=t:

                    if chat_id:

                        msg=f"""
رسول آقا!

زمان: {task}

{random.choice(motivation)}

خب بیا برویم!
"""

                        bot.send_message(chat_id,msg)

                    last_sent=t

        time.sleep(60)

# --------- Night report ---------

def night_report(bot):

    while True:

        now=datetime.now(tz)

        if now.strftime("%H:%M")=="22:30":

            if chat_id:

                bot.send_message(chat_id,
"""
رسول آقا 🌙

گزارش شبانه:

۱ امروز چند ساعت کار کردی؟
۲ روی دوره‌ها کار کردی؟
۳ فردا مهم‌ترین کارت چیست؟
""")

        time.sleep(60)

# --------- Start bot ---------

def start_bot():

    app=ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    bot=app.bot

    threading.Thread(target=reminder_loop,args=(bot,),daemon=True).start()

    threading.Thread(target=night_report,args=(bot,),daemon=True).start()

    app.run_polling()

# --------- Streamlit ---------

st.title("Rasul AI Coach")

st.write("Telegram Coach Bot is running...")

if "bot_started" not in st.session_state:

    threading.Thread(target=start_bot,daemon=True).start()

    st.session_state.bot_started=True
