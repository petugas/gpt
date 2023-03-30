import os
from dotenv import load_dotenv

load_dotenv()

print('started!')
NUMBERS_ROWS = 5

import openai
import telebot

openai.api_key = os.getenv('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')
bot = telebot.TeleBot(os.getenv('6219083756:AAGw0-Kjn-g7sw6dPW3e8OY7LRoutQdCcTA'))

if not os.path.exists("users"):
    os.mkdir("users")

@bot.message_handler(content_types=['text'])
def msg(message):
    if f"{message.chat.id}.txt" not in os.listdir('users'):
        with open(f"users/{message.chat.id}.txt", "x") as f:
            f.write('')

    with open(f'users/{message.chat.id}.txt', 'r', encoding='utf-8') as file:
        oldmes = file.read()

    if message.text == '/clear':
        with open(f'users/{message.chat.id}.txt', 'w', encoding='utf-8') as file:
            file.write('')
        return bot.send_message(chat_id=message.chat.id, text='clear history!')

    try:
        send_message = bot.send_message(chat_id=message.chat.id, text='processing request, please wait!')
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[{"role": "user", "content": oldmes},
                        {"role": "user","content": f'previous messages: {oldmes}; request: {message.text}'}], presence_penalty=0.6)

        bot.edit_message_text(text=completion.choices[0].message["content"], chat_id=message.chat.id, message_id=send_message.message_id)

        with open(f'users/{message.chat.id}.txt', 'a+', encoding='utf-8') as file:
            file.write(message.text.replace('\n', ' ') + '\n' + completion.choices[0].message["content"].replace('\n', ' ') + '\n')

        with open(f'users/{message.chat.id}.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if len(lines) >= NUMBERS_ROWS +1:
            with open(f'users/{message.chat.id}.txt', 'w', encoding='utf-8') as f:
                f.writelines(lines[2:])

    except Exception as e:
        bot.send_message(chat_id=message.chat.id, text=e)

bot.infinity_polling()
