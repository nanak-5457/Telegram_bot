from telegram.ext import Updater, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = '7569889638:AAGUXbQhTc7204KtYc0UAHO4S6UcJdDvA-E'

def solve_captcha(val1, val2):
    try:
        return str(int(val1) + int(val2))
    except:
        return ""

def report_group(link):
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 11)"}
    try:
        response = session.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        gpid = soup.find('input', {'name': 'gpid'})['value']
        code = soup.find('input', {'name': 'code'})['value']
        key = soup.find('input', {'name': 'key'})['value']
        val1 = soup.find('input', {'name': 'val1'})['value']
        val2 = soup.find('input', {'name': 'val2'})['value']
        captcha_answer = solve_captcha(val1, val2)
        data = {
            'gpid': gpid, 'code': code, 'key': key,
            'reason': 'Fake/Spam/Fraud',
            'rdesc': 'This is a spam group spreading harmful content.',
            'val1': val1, 'val2': val2, 'val3': captcha_answer
        }
        report_url = "https://groupsor.link/data/addreport"
        post = session.post(report_url, data=data, headers=headers)
        if "Thank you" in post.text:
            return "[SUCCESS] Group reported."
        elif "Please try after 1 minute" in post.text:
            return "[WAIT] Try after 1 minute."
        else:
            return "[FAILED] Report failed."
    except Exception as e:
        return f"[ERROR] {e}"

def handle_message(update, context):
    link = update.message.text.strip()
    if "groupsor.link/group/invite" in link or "t.me" in link:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"[PROCESSING] {link}")
        result = report_group(link)
        context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid link.")

updater = Updater(BOT_TOKEN)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
updater.start_polling()
updater.idle()
