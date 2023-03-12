
# TELEGRAM BOT 

Создать файл .env в корне проекта и оределить там переменные окружения 
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_GPT3_API_KEY = "YOUR_CHAT_GPT3_API_KEY"
id пользователей, которым будет доступен чат. @getmyid_bot
USERS_ID = ["user_id_1", 'user_id_2']  
ADMIN_USERNAME - "ADMIN_TELEGRAM_USERNAME.
------------------------------------------
В меню @BotFather добавить команды
variant - Description
deletecontext - Description
start - Description
--------------------

# ChatGPT 

gpt-3.5-turbo
--------------
"role": "system", "content" : "You're a kind helpful assistant. Answer as concisely as possible."
Опреелите как будет вести себя ваш ИИ.
----------------------------------------------
Максимальное количество токенов для генерации
https://platform.openai.com/tokenizer
max_tokens = 1000
-------------------------------------
Используемая температура отбора проб. 
Ближе 1 - больше креативности. 
Ближе к 0 - чётко определённые ответы.
temperature = 0.7
-----------------
Количество вариантов, которые необходимо 
сгенерировать для каждого входного сообщения.
n = 1

# DALL-E 

256×256	 0,016 $
512×512	 0,018 $
1024×1024 0,020 $

Если закоментить строку response_format
Изображение нужно будет заскачать response["data"][0]["url"]
-------------------------------------------------------------

