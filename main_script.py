import os
from flask import Flask, request
import telebot
import json


#TOKEN = os.environ.get('TOKEN')
#bot = telebot.TeleBot(TOKEN)

TOKEN = '1243846647:AAErXaEeJODvimG7HhPBbRZPVsIGWCT6z60'
bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

with open('courses.txt') as file:
    courses = [item.split(',') for item in file]
with open('planning.json', encoding="utf8") as json_file:
    data = json.load(json_file)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'PROG.Kyiv.UA')


@bot.message_handler(commands=['help'])
def help(message):
    res = '/courses - список курсов \n' \
          '/planning - расписание запуска курсов,'
    bot.reply_to(message, res)


@bot.message_handler(commands=['courses'])
def echo_message_courses(message):

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

    for text, url in courses:
        url_button = telebot.types.InlineKeyboardButton(text=text, url=url.strip(' \n'))
        keyboard.add(url_button)
    bot.send_message(message.chat.id, "Привет! Выбери курс", reply_markup=keyboard)

@bot.message_handler(commands=['planning'])
def echo_message_planning(message):

    res = ''
    for item in data['courses']:
        res += f"<b>{item['course']}</b>\n" \
                   f"<i>Online:</i> <code>{item['schedule']['online']}</code>\n" \
                   f"<i>Offline:</i> <code>{item['schedule']['offline']}</code>\n"
    bot.send_message(message.from_user.id, text=res, parse_mode='HTML')


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Python Telegram Bot 21-11-2020", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://https://yutestbot2211.herokuapp.com/' + TOKEN)
    return "Python Telegram Bot 21-11-2020", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
