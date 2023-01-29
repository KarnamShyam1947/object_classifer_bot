import requests
import Keys

telegram_bot_token = Keys.keys['telegram_token']
chat_id = Keys.keys['chat_id']
sendPhoto_url = Keys.urls['telegram_sendPhoto'].format(telegram_bot_token, chat_id)

def main():
    parameters = {
        'photo' : open('result.png', 'rb')
    }

    response = requests.post(url=sendPhoto_url, files=parameters)
    print(response)

if __name__ == '__main__' : 
    main()