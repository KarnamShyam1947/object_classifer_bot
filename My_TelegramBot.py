from datetime import datetime
from telegram.ext import *
import Recognition
import requests
import Keys
import csv

telegram_bot_token = Keys.keys['telegram_token']

telegram_getUpdate = Keys.urls['telegram_getUpdate'].format(telegram_bot_token)
telegram_sendPhoto_base = Keys.urls['telegram_sendPhoto']

def log_chat_info(row):
    with open('telegram_chat_logs.csv', 'a',newline='') as file:
        writer =csv.writer(file)
        writer.writerow(row)
    file.close()

def log_message_info(update):
    msg = str(update.message.text).lower()
    date_and_time = datetime.now().strftime(' %d-%m-%Y, %H:%M:%S ')
    chat_type = update.message.chat.type

    if chat_type == 'group':
        response = requests.get(telegram_getUpdate).json()
        chat_id = response['result'][0]['message']['from']['id']
        first_name = response['result'][0]['message']['from']['first_name']
        last_name = response['result'][0]['message']['from']['last_name']
        print(f'[ {date_and_time}] User {first_name} {last_name} with chat id {chat_id}, send message "{msg}" in {chat_type}')
        row = [date_and_time, chat_id, first_name, last_name, msg, chat_type]
        log_chat_info(row)

    else:
        chat_id = update.message.chat.id
        first_name = update.message.chat.first_name
        last_name = update.message.chat.last_name
        print(f'[ {date_and_time}] User {first_name} {last_name} with chat id {chat_id}, send message "{msg}" in {chat_type}')
        row = [date_and_time, chat_id, first_name, last_name, msg, chat_type]
        log_chat_info(row)

def log_image_info(update):
    date_and_time = datetime.now().strftime(' %d-%m-%Y, %H:%M:%S ')
    chat_type = update.message.chat.type
    msg = update.message.caption

    if chat_type == 'group':
        response = requests.get(telegram_getUpdate).json()
        chat_id = response['result'][0]['message']['from']['id']
        first_name = response['result'][0]['message']['from']['first_name']
        last_name = response['result'][0]['message']['from']['last_name']
        print(f'[ {date_and_time}] User {first_name} {last_name} with chat id {chat_id}, send photo with caption "{msg}" in {chat_type}')
        row = [date_and_time, chat_id, first_name, last_name, msg, chat_type]
        log_chat_info(row)

    else:
        chat_id = update.message.chat.id
        first_name = update.message.chat.first_name
        last_name = update.message.chat.last_name
        print(f'[ {date_and_time}] User {first_name} {last_name} with chat id {chat_id}, send photo with caption "{msg}" in {chat_type}')
        row = [date_and_time, chat_id, first_name, last_name, msg, chat_type]
        log_chat_info(row)

def handle_response(msg):
    if msg in ['hi', 'hii', 'hello', 'hlo']:
        return 'Hii, How can i help you...?'

    elif 'how are you' in msg:
        return 'I am good, Thanks for asking....'

    elif 'bye' in msg:
        return 'Bye....!!!\nThanks for visiting me'

    else:
        return 'You said : {}'.format(msg)

def send_result_photo(chat_id):
    telegram_sendPhoto_final = telegram_sendPhoto_base.format(telegram_bot_token, chat_id)

    data = {
        'photo' : open('result.png', 'rb')
    }

    resp = requests.post(telegram_sendPhoto_final, files=data)

def handle_start(update, context):
    log_message_info(update)
    update.message.reply_text("Hii, I am Object classify bot")

def handle_help(update, context):
    log_message_info(update)
    update.message.reply_text("Try to send me photo of object, I will classify")


def handle_message(update, context):
    log_message_info(update)
    msg = str(update.message.text).lower()
    resp = handle_response(msg)

    update.message.reply_text(resp)


def handle_image(update, context):
    log_image_info(update)
    chat_id = str(update.message.chat.id)
    photo = update.message.photo[-1].get_file()
    photo.download("img.jpg")

    model = Recognition.load_model()
    path = "img.jpg"
    conf = 0.6

    response, resp_str = Recognition.detect_labels(path, conf, model)
    if response:
        send_result_photo(chat_id)

    update.message.reply_text(resp_str)
        
def handle_error(update, context):
    date_and_time = datetime.now().strftime(' %d-%m-%Y, %H:%M:%S ')
    print(f'[ {date_and_time} ] Update {update} caused error {context.error}')

def start_bot():

    updater = Updater(telegram_bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', handle_start))
    dp.add_handler(CommandHandler('help', handle_help))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.photo, handle_image))

    dp.add_error_handler(handle_error)

    updater.start_polling(1.0)
    updater.idle()

def main():
    print('Telegram bot started......')

    start_bot()

if __name__ == '__main__' : 
    main()