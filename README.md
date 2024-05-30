# Тестовое задание: pyrogram ЮЗЕР-бот

### Необходимые библиотеки:
Все указаны в requirements.txt, но для общего понимания будут продублированы здесь:\

**python 3.10** - из-за библиотеки **tgcrypto**. С ней pyrogram работает быстрее, но на версиях 3.11+ 
она пока не работает. Можно использовать python 3.11 и выше, но без tgcrypto. Работать будет, но pyrogram будет ругаться.

psycopg2-binary == 2.9.9 - необходим для работы sqlalchemy с postgres\
sqlalchemy == 2.0.30\
pyrogram == 2.0.10\
asyncpg == 0.29.0 - асинхронный драйвер для sqlalchemy - postgres\
loguru == 0.7.2 - красивые и удобные логи\
sqlalchemy-utils == 0.41.2 - ChoiceType и ещё куча полезных штук\
tgcrypto == 1.2.5 \
python-dotenv == 1.0.1 - для работы с .env файлами. Особенно удобен в Windows


### Установка


#### При использовании без docker-контейнера:
Подразумевая, что уже есть установленный python 3.9+ \
Подготовьте виртуальное окружение:
```
python -m venv venv
```
Активируйте venv
###### Linux
```chatinput
source venv/bin/activate
```
###### Windows
```venv\Scripts\activate```

Устанавливаем зависимости:


```pip install -r requirements.txt```

В папке /bot заполнить .envTEMPLATE и переименовать в .env\
в файле settings.py раскомментировать строчки\
```
from dotenv import load_dotenv()
load_dotenv()
```
Дальше всё просто:
Меняем папку на /bot и\
```python main.py```

#### При использовании docker:
###### ПЕРВЫЙ ЗАПУСК
<ol>
<li>Заполнить .envTEMPLATE, переименовать в .env</li>
<li>Запустить команду <pre>docker compose run pyro_bot</pre>
<b>Запускать нужно исключительно run, потому, что при первом запуске pyrogram требует код подтверждения от телеграмма (КОД ПРИХОДИТ В ТЕЛЕГРАМ, НЕ ПО СМС) После успешного создания сессии такого больше не будет</b></li>
</ol>
В docker-compose.yaml прописан сразу и postgres, если будете использовать готовый - нужно будет удалить строчки в docker-compose.yaml

```chatinput
depends on:
    postgres:
        condition: service_healthy
```
И указать свои данные в .env файле для postgres
###### Последующие запуски:
```chatinput
docker compose up
```

Переменные .env:
<pre>
APP_NAME          - Имя приложения. По этому названию pyrogram будет хранить файл сессии в файле [APP_NAME].sessio\
API_ID            - ID бота получаем на https://my.telegram.org/ 
API_HASH          - Хэш бота на https://my.telegram.org/ 
POSTGRES_USER     - Ваше имя пользователя в postgres
POSTGRES_PASSWORD - Пароль
POSTGRES_DB       - название СУЩЕСТВУЩЕЙ базы данных
POSTGRES_HOST     - хост на котором у Вас postgres
POSTGRES_PORT     - порт соответственно
DEBUG             - 0 - минимизированные логи, 1 - расширенные
</pre>

ЛИЦЕНЗИЯ MIT





