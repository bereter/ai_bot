# Проект SpeechLand app


## Настройка проекта перед запуском

Перед началом работы необходимо установить библиотеки и зависимости в виртуальное окружение
`pip install -r requirements.txt`

Далее в корне проекта необходимо создать файл `.env` и в нем прописать следующие параметры для базы данных и проекта:

```
DB_POSTGRES=postgresql+asyncpg://"имя пользователя":"пароль"@"хост":"порт"/"имя базы данных"
DB_POSTGRES_ALEMBIC=postgresql://"имя пользователя":"пароль"@"хост":"порт"/"имя базы данных"

KEY_GIGA_CHAT="Ключ от Gigachat"

JWT_SECRET="Секретный ключь"
ALGORITHM="Алгоритм шифрования"
```

И наконец применить миграции. Для этого, находясь в папке `fast_app` , необходимо прописать в терминале команду `alembic upgrade head`

---