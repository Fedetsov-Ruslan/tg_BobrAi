## Telegram Bot + RestApi написанное на FastAPI

# Функционал телеграмм бота:
 
 - Делать запросы через API OpenWeatherMap и получать в ответ погоду во введенном городе в данное время
    используя команду /weather <город>. Например /weather Москва
 - Сохранять необходимый город по команде /save. После которой поросит ввести название города который хотим сохранить
 - Получать информацию в сохраненном  ранее городе по команде /mycity

# функционал API
 
 - Получить все данные через endpoint "/logs"
 - Получить все данные для конкретного пльзователя через endpoint "/logs/{user_id} 

 (Я реализовал через FastAPI потому что по необходимости его намного проще интегрировать в любую систему. 
  Если надо реализовать вывод и пагинацию в самом телеграмм. 
  То можно использовать webhook и через ngrok связать fastapi приложение и бота 
  и уже там реализовать пагинацию.)
  Так как пользователь впринципе не должен иметь доступ к таким данным я не видел целесообразноть добавдять этот функцционал в сам бот.

# Инструкции по запуску на локальной машине
 - Создать файл .env, перенести из Файла .env.example переменные и задать их.
 - Установить все зависимости из файла requirements.txt командой  "pip install -r requirements.txt"
 - Запустить redis на адресе localhost:6379 (можно запустить docker desctop и активировать командой "docker run -d --name <contener_name> -p 6379:6379 redis")
 - Запустить бота командой "python run.py"
 - Запустить RESTapi командой "pytthon restapi.py"
 - API находится на хосте http://127.0.0.1:8000/docs#/

 # Запуск через docker-compose
  - Создать файл .env, перенести из Файла .env.example переменные и задать их.
  - Изменить REDIS_URL=redis://loacalhost:6379 на REDIS_URL=redis://redis:6379
  - Изменить DB_HOST=loacalhost на DB_HOST=db
  - Сбилдить docker контейнер для приложения командой "docker build -t tg_fastapi_weather_bot:latest . "
  - Запустить командой "docker-compose up --build"
  - API находится на хосте http://127.0.0.1:8000/docs#/

 # Реализованны тесты
 - команда запуска "pytest tests/"

