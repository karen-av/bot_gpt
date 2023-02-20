from telebot import TeleBot, types
from functions import respotnse_gpt, check_user
import openai
import os

USERS_ID = ('502197389')
openai.api_key = os.getenv('CHAT_GPT3_API_KEY')
bot = TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
CHAT_GPT3_API_KEY="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"
TELEGRAM_BOT_TOKEN="6207234187:AAFLgWV1UJ2TzugXH1JRCxLuZOC4qfZe7-8"

item1 = types.KeyboardButton('/start')
item2 = types.KeyboardButton('/help')
item3 = types.KeyboardButton('/story')
item4 = types.KeyboardButton('/users')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if check_user(message.from_user.id):
        markup.add(item1)
        bot.send_message(message.chat.id, "Привет, {0.first_name}!\
            \nОтправь сообщение с вопросом для ChatGPT.\
            \nДля управления списом пользователей нажмите Users.\
            ".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
    else:
        markup.add(item1)
        bot.send_message(message.chat.id, "Привет, {0.first_name}!\
            \nДля доступа к чату тебе нужно получить доступ у админа.\
            ".format(message.from_user), parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(item1)
    bot.reply_to(message, "Раздел в разработке.",reply_markup=markup)


@bot.message_handler(commands=['story'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(item1)
    bot.reply_to(message, "Раздел в разработке.",reply_markup=markup)


@bot.message_handler(commands=['users'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(item1)
    bot.reply_to(message, "Раздел в разработке.",reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.chat.type == 'private' and check_user(message.from_user.id):
        markup.add(item1)
        response = respotnse_gpt(message.text)
        output_text = response.choices[0].text
        bot.send_message(message.chat.id, output_text, reply_markup=markup)
    else:
        markup.add(item1)
        bot.send_message(message.chat.id, "\
            \nДля доступа к чату тебе нужно получить доступ у админа.\
            ".format(message.from_user), parse_mode='html', reply_markup=markup)

if __name__ == "__main__":
    bot.polling(none_stop=True)
    
    
