import openai
import sqlite3


def check_user(user_id, USERS_ID):
    if str(user_id) in USERS_ID:
        return True
    return False


def connection_db():
    try:
        connection = sqlite3.connect('sqlite.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS gpt (
                                    id INTEGER PRIMARY KEY,
                                    user_id TEXT,
                                    assistant TEXT);''')
        cursor.close()
        return connection
    except:
        return False


def insert_db(user_id, assist_text):
    val = (user_id, assist_text,)
    connection = connection_db()
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO gpt (user_id, assistant)  VALUES  (?, ?)", val)
        connection.commit()
        cursor.close()
    except Exception as _ex:
            print("[INFO] Error while working with SQLite", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] SQLite connection closed")


def select_db(user_id):
    user_id = (user_id, )
    connection = connection_db()
    try:
        cursor = connection.cursor()
        result = cursor.execute("SELECT assistant FROM gpt WHERE user_id=?", user_id).fetchall()
        cursor.close()
        return result
    except Exception as _ex:
            print("[INFO] Error while working with SQLite", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] SQLite connection closed")


def dell_db(user_id):
    user_id = (user_id, )
    connection = connection_db()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM gpt WHERE user_id=?", user_id)
        connection.commit()
        cursor.close()
    except Exception as _ex:
            print("[INFO] Error while working with SQLite", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] SQLite connection closed")


def respotnse_gpt(user_id, content):
    messages = [{"role": "system", "content" : "You're a kind helpful assistant. Answer as concisely as possible."}]
    assistant = select_db(user_id)
    for assist in assistant:
         messages.append({"role": "assistant", "content": assist[0]})
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=messages
    #max_tokens=1000
    #temperature = 0.7
    #n = 1
    )
    chat_response = completion.choices[0].message.content
    insert_db(user_id, chat_response)
    return chat_response


    # Максимальное количество токенов для генерации при завершении (здесь вы можете увидеть токенизатор, который использует OpenAI) https://platform.openai.com/tokenizer
    #max_tokens=1000
    # Используемая температура отбора проб. Значения, близкие к 1, придадут модели больше риска / креативности, в то время как значения, близкие к 0, будут генерировать чётко определённые ответы.
    # Количество вариантов завершения общения, которые необходимо сгенерировать для каждого входного сообщения.
    #temperature = 0.7
    #n = 1

