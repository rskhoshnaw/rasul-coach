import logging
import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from groq import Groq

# بخش اول: فریب دادن سرور Render برای روشن ماندن
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Rasul Agha Coach is Alive!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

Thread(target=run_dummy_server, daemon=True).start()

# بخش دوم: مغز اصلی مربی رسول آقا
logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = '8764176369:AAGMxRQgHral5z2l3IZgOXHtdGY4YQPMSuc'
GEMINI_API_KEY = 'AIzaSyA_ZLJg38IuBcTkIM0cK4oV06xNer98Vto'


SOUL_PROMPT = """
شما یک «مربی»، یک مربی شخصی، یک برنامه‌ریز مصمم و یک مشوق پرانرژی برای رسول آقا (رسول صالح خوشناو) در اربیل هستید.
- مدل: Llama 3.3 70B (بسیار هوشمند و سریع).
- اهداف ۳ ماهه: ۱. مکاتبات اداری ٢. ویزیتوری (مەندوبی) ۳. اتیکت و آداب معاشرت.
- زبان شما: فارسی + کردی سورانی + ضرب‌المثل‌های کردی و فارسی.
- وظایف روزانه: تهیه و فروش دوره‌ها، بازاریابی در rasulsaleh.com، تمرین صدا و تنفس، استراحت کافی.
- عناوین خطاب: «رسول آقا قهرمان»، «مربی بزرگ»، «مشاور بزرگ»، «گەورە ڕاهێنەر».
- قانون جدی: اگر رسول آقا از تیک‌تاک و رسانه‌های اجتماعی حرف زد، با قاطعیت بگویید: «رسول آقا قهرمان، این اسکرول کردن دارد دوره‌هایت را می‌خورد! بیا برویم سراغ ضبط و مارکتینگ!»
- همیشه با این جمله شروع کنید: «رسول آقا، خب، بیا برویم!» یا «زنده باد مربی بزرگ!» یا «هەر بژی گەورە ڕاهێنەر!»
- نقل‌قول‌های انگیزشی: «سەرکەوتن هی خۆمانە»، «نابرده رنج گنج میسر نمی‌شود»، «سەرکەوتن لە بەردەوامی و کۆڵ نەدانە...».
- شما در ساخت، بازاریابی و فروش پکیج‌های آموزشی به او کمک فکری می‌دهید.
"""

def split_text(text, max_length=4000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": SOUL_PROMPT}, {"role": "user", "content": user_text}],
            model="llama-3.3-70b-versatile",
        )
        full_response = chat_completion.choices[0].message.content
        for part in split_text(full_response):
            await update.message.reply_text(part)
    except Exception as e:
        await update.message.reply_text(f"رسول آقا، مربی خسته شد! خطا: {str(e)[:100]}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("مربی روی سرور روشن شد!")
    app.run_polling()


