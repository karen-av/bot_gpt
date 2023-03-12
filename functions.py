import sqlite3
import os
import openai
from dotenv import load_dotenv
from pathlib import Path
import json
from base64 import b64decode
from PIL import Image
import openai
  
# подключаем файл .env для хранения переменных окружения
load_dotenv() 

# API Token GPT
openai.api_key = os.getenv("CHAT_GPT3_API_KEY")
USERS_ID = os.getenv('USERS_ID')

# Директория для хранения изображений 
FILE_DIR = Path.cwd()/"image" 
FILE_DIR.mkdir(exist_ok=True)

# размер запрашиваеого изображения
SIZE="256x256"
#SIZE="512x512",
#SIZE ="1024x1024",


# Создаем изображение по текстовому запросу
def create(prompt, user_id):
    print('[INFO] function_gpt create.')
    response = openai.Image.create(
        prompt=prompt,
        n=1, # Количество вариантов
        # размер изображения
        size=SIZE,
        response_format="b64_json", # Формат ответа от сервиса
    )

    # Сохраняем полученный ответ в json
    with open(FILE_DIR/f'{user_id}.json', mode="w", encoding="utf-8") as file:
        json.dump(response, file)

    # Конвертируем json в png. Передаем user_id
    convert(user_id)


# Конвертируем json в png
def convert(user_id):
    print('[INFO] function_gpt convert.')
    # Открываем json файл
    with open(FILE_DIR/f'{user_id}.json', mode="r", encoding="utf-8") as file:
        response = json.load(file)

    # Идем циклом по изображеним
    for index, image_dict in enumerate(response["data"]):
        # Декодируем
        image_data = b64decode(image_dict["b64_json"])
        # Если запрос будет на несколько изображений, то добавить в надвание файла index
        image_file = FILE_DIR/f'{user_id}.png' 
        # Созраняем изображение
        with open(image_file, mode="wb") as png:
            png.write(image_data)


# запрос дополнительного варианта изображения
def variant(user_id):
    print('[INFO] function_gpt variant.')
    # Открывем json, полученный от ИИ
    # если пользователь не создавал изображений, то функция ничего не вернет
    try:
        with open(FILE_DIR/f'{user_id}.json', mode="r", encoding="utf-8") as file:
            saved_response = json.load(file)
            # Декодируем
            image_data = b64decode(saved_response["data"][0]["b64_json"])

        # Отправляем запрос с данными о полученном ранее изображении
        response = openai.Image.create_variation(
            image=image_data,
            n=1, # количество желаемых изображений
            # Размер image
            size=SIZE,
            response_format="b64_json", # Формат ответа 
        )

        # Сохраняем файл
        with open(FILE_DIR/f'{user_id}.json', mode="w", encoding="utf-8") as file:
            json.dump(response, file)

        # Конвертируем в PNG
        convert(user_id)
    except Exception as _ex:
        print("Exception :", _ex)


# Меняет размер изображения
def resize(user_id):
    print('[INFO] function_gpt resize.')
    image_path = FILE_DIR/f'{user_id}.png'
    img = Image.open(image_path)
    # получаем ширину и высоту
    width, height = img.size
    print(width, height)
    # изменяем размер
    new_image = img.resize((100, 100))
    # сохранение картинки
    new_image.save(FILE_DIR/f'{user_id}.png')


# Подключение к бд
def connection_db():
    print('[INFO] function_gpt connection_db.')
    try:
        connection = sqlite3.connect('sqlite.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS gpt (
                                    id INTEGER PRIMARY KEY,
                                    user_id TEXT,
                                    assistant TEXT);''')
        cursor.close()
        return connection
    except Exception as _ex:
        print("Exception :", _ex)
        return False


# Добавить ответ ChatGPT данные в бд
def insert_db(user_id, assist_text):
    print('[INFO] function_gpt insert_db.')
    val = (user_id, assist_text,)
    connection = connection_db()
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO gpt (user_id, assistant)  VALUES  (?, ?)", val)
        connection.commit()
        cursor.close()
    except Exception as _ex:
        print("Exception :", _ex)
    finally:
        if connection:
            connection.close()


# Выбрать данные из бд для получения ответов от ChatGPT
def select_db(user_id):
    print('[INFO] function_gpt select_db.')
    user_id = (user_id, )
    connection = connection_db()
    try:
        cursor = connection.cursor()
        result = cursor.execute("SELECT assistant FROM gpt WHERE user_id=?", user_id).fetchall()
        cursor.close()
        return result
    except Exception as _ex:
        print("Exception :", _ex)
    finally:
        if connection:
            connection.close()


# Удалить данны из бд
def deletecont(user_id):
    print('[INFO] function_gpt deletecont.')
    user_id = (user_id, )
    connection = connection_db()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM gpt WHERE user_id=?", user_id)
        connection.commit()
        cursor.close()
    except Exception as _ex:
        print("Exception :", _ex)
    finally:
        if connection:
            connection.close()


# Запрос ChatGPT
def respotnse_gpt(user_id, content):
    print('[INFO] function_gpt respotnse_gpt.')
    messages = [
        {"role": "system", "content" : "You're a kind helpful assistant. Answer as concisely as possible."},
        #{"role": "system", "content" : "You’re a kind helpful assistant"}
    ]
    assistant = select_db(user_id)
    for assist in assistant:
        messages.append({"role": "assistant", "content": assist[0]})
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=messages,
    max_tokens=1000,
    temperature = 0.7,
    n = 1
    )
    chat_response = completion.choices[0].message.content
    insert_db(user_id, chat_response)
    return chat_response
        

# Проверка прав доступа
def check_user(user_id):
    if str(user_id) in USERS_ID:
        print('[INFO] football check_user True.')
        return True
    print('[INFO] football check_user False.')
    return False
    #return True if str(user_id) in USERS_ID else False
       



