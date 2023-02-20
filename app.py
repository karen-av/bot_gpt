from telebot import TeleBot, types
from functions import respotnse_gpt, check_user
import openai
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

USERS_ID = os.getenv('USERS_ID')
openai.api_key = os.getenv("CHAT_GPT3_API_KEY")
bot = TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

item1 = types.KeyboardButton('/start')
item2 = types.KeyboardButton('/help')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if check_user(message.from_user.id, USERS_ID):
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Привет, {0.first_name}!\
            \nОтправь сообщение с вопросом для ChatGPT.\
            ".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
    else:
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Привет, {0.first_name}!\
            \nДля доступа к чату тебе нужно получить доступ у админа.\
            ".format(message.from_user), parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(item1, item2)
    bot.reply_to(message, "Раздел в разработке.",reply_markup=markup)


@bot.message_handler(commands=['story'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(item1, item2)
    bot.reply_to(message, "Раздел в разработке.",reply_markup=markup)


@bot.message_handler(commands=['users'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(item1, item2)
    bot.reply_to(message, "Раздел в разработке.",reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.chat.type == 'private' and check_user(message.from_user.id, USERS_ID):
        markup.add(item1, item2)
        response = respotnse_gpt(message.text)
        output_text = response.choices[0].text
        bot.send_message(message.chat.id, output_text, reply_markup=markup)
    else:
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "\
            \nДля доступа к чату тебе нужно получить доступ у админа.\
            ".format(message.from_user), parse_mode='html', reply_markup=markup)

if __name__ == "__main__":
    bot.polling(none_stop=True)
    
    
