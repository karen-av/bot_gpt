from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
import openai
import os
from functions import create, variant, FILE_DIR, respotnse_gpt, deletecont, check_user

load_dotenv()


bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher(bot)
openai.api_key = os.getenv("CHAT_GPT3_API_KEY")
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
PERMISSION_DENIDE = f"Для доступа к ChatGPT получить доступ у админа {ADMIN_USERNAME}."


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    print('[INFO] app start.')
    text_message = "Для запроса к ChatPGT отправь\
        \nсообщение с вопросом боту.\nНапиши боту /image + описание изображения и пришлет тебе картинку.\
        \nОтправьте боту /image и он вернет тебе последнее сделанное изображение.\
        \nКоманда /variant создаст еще один вариант последнего изображения."
    await bot.send_message(message.from_user.id, text_message)



# если запрос на все турниры на сегодня
@dp.message_handler(commands=['deletecontext'])
async def deletecontext(message: types.Message):
    print('[INFO] app deletecontext.')
    # Если пользователь есть в списке пользователей
    if check_user(message.from_user.id):
        deletecont(message.from_user.id)
        await bot.send_message(message.from_user.id, "Контекст удален")
        print('[INFO] app deletecontext - Контекст удален.')
    else:
        print('[INFO] app deletecontext - Пользователю отказано в доступе.')
        bot.send_message(message.chat.id, PERMISSION_DENIDE)
     

# Создать изображение
@dp.message_handler(commands=['image'])
async def image(message: types.Message):
    print('[INFO] app image.')

    # Если пользователь есть в списке пользователей
    if check_user(message.from_user.id):
        # готовим запрос отрезая от него /image
        prompt = str(message.text)[7:]

        # Если была команда /image + запрос если была только командаБ то высылаем посденее фото
        if len(prompt) != 0: 
            # Вызываем функцию генерации изображения и передаем ей запрос и user_id
            create(prompt, message.from_user.id)
        
        # открываем файл с изображением и отправляем пользователю. Имя файла основано на user_id
        try:    
            with open(FILE_DIR/f'{message.from_user.id}.png', mode="rb") as file:
                print('[INFO] app image display image.')
                await bot.send_message(message.chat.id, "DALL·E:")
                await bot.send_photo(message.chat.id, file)
        # если у пользователя еще нет фото
        except Exception as _ex:
            print("[INFO] Exception image :", _ex)
            await bot.send_message(message.chat.id, "Вы еще не создавали фото.")

    # Если пользователя нет в списке 
    else:
        print('[INFO] app image PERMISSION_DENIDE.')
        await bot.send_message(message.chat.id, PERMISSION_DENIDE)


# Создать изображение
@dp.message_handler(commands=['variant'])
async def start(message: types.Message):
    print('[INFO] app image.')
    # Проверка пользователя на право доступа
    if check_user(message.from_user.id):
        # Вызов функции, которая генерит еще один вариант последнего изображения
        variant(message.from_user.id)
        try:
            # Открываем соднанный файл и отправляем пользователю
            with open(FILE_DIR/f'{message.from_user.id}.png', mode="rb") as file:
                print('[INFO] app image display image.')
                await bot.send_message(message.chat.id, "DALL·E:")
                await bot.send_photo(message.chat.id, file)
        except Exception as _ex:
            print("[INFO] Exception image :", _ex)
            await bot.send_message(message.chat.id, "Бот еще не создавал изображения.")
    else:
        print('[INFO] app image PERMISSION_DENIDE.')
        await bot.send_message(message.chat.id, PERMISSION_DENIDE)


@dp.message_handler(content_types=['text'])
async def text_message(message: types.Message):
    print('[INFO] app message_handler text')
    if message.chat.type == 'private':
        # Если пользователь ввел дату
      
        # Если запрос к chatGPT
        #Проверка на право достпа пользователя к чату
        if check_user(message.from_user.id): 
            print('[INFO] app message_handler - chat_gpt')
            # Передаем запрос к чату через функцию
            try:
                response = respotnse_gpt(message.from_user.id, message.text)
                await bot.send_message(message.chat.id, f"CharGPT:\n{response}")
            except Exception as _ex:
                print("Exception :", _ex)
                await bot.send_message(message.chat.id, f"Ошибка. Обратитесь к системному администратору {ADMIN_USERNAME}.")
        
        # Отказано в доступе
        else:
            print('[INFO] app message_handler - PERMISSION_DENIDE')
            await bot.send_message(message.chat.id, PERMISSION_DENIDE)

    else:
        await bot.send_message(message.from_user.id, f'echo: {message.text}')


        

if __name__ == '__main__':
    executor.start_polling(dp)
    
