import streamlit as st
import google.generativeai as genai
from telegram.ext import Updater, MessageHandler, Filters
import threading
import time
from datetime import datetime
import pytz
import random

# -------------------
# Secrets
# -------------------

TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
GEMINI_KEY = st.secrets["GEMINI_KEY"]

# -------------------
# Gemini
# -------------------

genai.configure(api_key=GEMINI_KEY)

model = None

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    print("Gemini init error:", e)

# -------------------
# Timezone
# -------------------

tz = pytz.timezone("Asia/Baghdad")

# -------------------
# User Data
# -------------------

chat_id = None
last_user_message = time.time()

# -------------------
# System Prompt
# -------------------

SYSTEM_PROMPT = """
تو مربی شخصی رسول صالح خوشناو هستی.

نام او: رسول آقا

لحن:
فارسی + کوردی سورانی
انرژی بالا
قاطع و انگیزشی

تکیه کلام ها:
رسول آقا، خب، بیا برویم!
سەرکەوتن هی خۆمانە

اهداف ۳ ماهه:

1 ضبط دوره مکاتبات اداری
2 ضبط دوره ویزیتوری
3 ضبط دوره اتیکت

وظیفه:
جلوگیری از تنبلی
تمرکز روی تولید دوره
تمرکز روی بازاریابی rasulsaleh.com
"""

# -------------------
# Schedule
# -------------------

schedule = {

"Saturday":[
("07:00","ورزش"),
("07:30","تمرین صدا"),
("08:00","برنامه ریزی روز"),
("09:00","تهیه دوره"),
("13:00","مکاتبات اداری"),
("18:30","بازاریابی سایت"),
("21:00","دیدار والدین")
],

"Tuesday":[
("07:00","ورزش"),
("07:30","تمرین صدا"),
("08:00","برنامه ریزی"),
("09:00","تهیه دوره"),
("13:00","مکاتبات اداری"),
("18:30","بازاریابی سایت"),
("21:00","دیدار والدین")
],

"Sunday":[
("08:00","رفتن به اداره"),
("10:00","تمرکز در اداره"),
("12:00","ادامه کار"),
("16:00","تمرین صدا"),
("17:00","تهیه دوره"),
("20:00","بازاریابی سایت"),
("21:00","دیدار والدین")
],

"Monday":[
("08:00","رفتن به اداره"),
("10:00","تمرکز در اداره"),
("12:00","ادامه کار"),
("16:00","تمرین صدا"),
("17:00","تهیه دوره"),
("20:00","بازاریابی سایت"),
("21:00","دیدار والدین")
]

}

# -------------------
# Motivational messages
# -------------------

motivation = [

"رسول آقا! تمرکز! امروز آینده ساخته می‌شود.",
"TikTok صبر می‌کند، موفقیت نه!",
"سەرکەوتن هی خۆمانە 🔥",
"یک ساعت تمرکز = یک قدم به آزادی مالی",
"رسول آقا خب بیا برویم!"
]

# -------------------
# Telegram handler
# -------------------

def handle_message(update, context):

    global chat_id,last_user_message

    chat_id = update.message.chat_id
    user_text = update.message.text

    last_user_message = time.time()

    prompt = SYSTEM_PROMPT + "\nUser:" + user_text

    try:

        response = model.generate_content(prompt)

        reply = response.text

    except Exception as e:

        reply = f"""
رسول آقا ⚠️

خطا در ارتباط با هوش مصنوعی

{str(e)}

بعداً دوباره امتحان کن
"""

    update.message.reply_text(reply)

# -------------------
# Reminder Engine
# -------------------

def reminder_loop(bot):

    last_sent = ""

    while True:

        now = datetime.now(tz)

        day = now.strftime("%A")
        current = now.strftime("%H:%M")

        if day in schedule:

            for t,task in schedule[day]:

                if t == current and last_sent != current:

                    if chat_id:

                        msg = f"""
رسول آقا!

زمان:
{task}

{random.choice(motivation)}

خب بیا برویم!
"""

                        bot.send_message(chat_id,msg)

                    last_sent = current

        time.sleep(60)

# -------------------
# Anti procrastination
# -------------------

def focus_guard(bot):

    while True:

        if chat_id:

            idle = time.time() - last_user_message

            if idle > 7200:

                bot.send_message(chat_id,
                """رسول آقا!

۲ ساعت است از تو خبری نیست.

آیا روی دوره‌ها کار می‌کنی یا وقت در شبکه‌های اجتماعی می‌گذرد؟

سەرکەوتن هی خۆمانە
""")

        time.sleep(1800)

# -------------------
# Night report
# -------------------

def night_report(bot):

    while True:

        now = datetime.now(tz)

        if now.strftime("%H:%M") == "22:30":

            if chat_id:

                bot.send_message(chat_id,
"""
رسول آقا 🌙

وقت گزارش شبانه است.

امروز:

۱ چند ساعت روی دوره‌ها کار کردی؟
۲ آیا بازاریابی سایت انجام شد؟
۳ فردا چه کاری مهم‌تر است؟

جواب بده تا برنامه فردا را تنظیم کنیم.
""")

        time.sleep(60)

# -------------------
# Start bot
# -------------------

def start_bot():

    updater = Updater(TELEGRAM_TOKEN,use_context=True)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text,handle_message))

    updater.start_polling()

    bot = updater.bot

    threading.Thread(target=reminder_loop,args=(bot,),daemon=True).start()
    threading.Thread(target=focus_guard,args=(bot,),daemon=True).start()
    threading.Thread(target=night_report,args=(bot,),daemon=True).start()

    updater.idle()

# -------------------
# Streamlit
# -------------------

st.title("AI Coach for Rasul Saleh")

st.write("Bot running...")

if "bot_started" not in st.session_state:

    threading.Thread(target=start_bot,daemon=True).start()

    st.session_state.bot_started=True
