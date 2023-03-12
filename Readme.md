
# TELEGRAM BOT 

<p>Создать файл .env в корне проекта и оределить там переменные окружения <br>
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"<br>
CHAT_GPT3_API_KEY = "YOUR_CHAT_GPT3_API_KEY"<br>
id пользователей, которым будет доступен чат. @getmyid_bot<br>
USERS_ID = ["user_id_1", 'user_id_2']  <br>
ADMIN_USERNAME - "ADMIN_TELEGRAM_USERNAME.<br>
------------------------------------------<br>
В меню @BotFather добавить команды<br>
variant - Description<br>
deletecontext - Description<br>
start - Description<br>
--------------------<p>

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

