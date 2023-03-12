
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

<p>gpt-3.5-turbo<br>
--------------<br>
"role": "system", "content" : "You're a kind helpful assistant. Answer as concisely as possible."<br>
Опреелите как будет вести себя ваш ИИ.<br>
----------------------------------------------<br>
Максимальное количество токенов для генерации<br>
https://platform.openai.com/tokenizer<br>
max_tokens = 1000<br>
-------------------------------------<br>
Используемая температура отбора проб. <br>
Ближе 1 - больше креативности. <br>
Ближе к 0 - чётко определённые ответы.<br>
temperature = 0.7<br>
-----------------<br>
Количество вариантов, которые необходимо <br>
сгенерировать для каждого входного сообщения.<br>
n = 1</p>

# DALL-E 

<p>256×256	 0,016 $<br>
512×512	 0,018 $<br>
1024×1024 0,020 $<br>

Если закоментить строку response_format<br>
Изображение нужно будет заскачать response["data"][0]["url"]<br>
-------------------------------------------------------------</p>