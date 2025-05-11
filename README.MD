# Currency Service

Асинхронный сервис для получения курсов валют и управления балансом различных валют.

## Стек

* **Python** 3.11
* **FastAPI** для REST API
* **HTTPX** для выполнения HTTP-запросов к внешнему API
* **Pydantic** + **pydantic-settings** для валидации схем и конфигураций
* **logging** для ведения логов (консоль + файл)
* **Black**, **Flake8** для форматирования

## Возможности

* Периодическое (каждые N минут) получение курсов валют с публичного API (ЦБ РФ) по умолчанию `https://www.cbr-xml-daily.ru/daily_json.js`.
* Поддержка нескольких валют (по умолчанию: RUB, USD, EUR) с возможностью расширения.
* CLI для задания начального баланса каждой валюты и периода обновления курсов.
* REST API для управления балансом и получения сводной информации:

  * **GET** `/api/v1/{currency}/get/` — получить текущий баланс валюты.
  * **GET** `/api/v1/amount/get/` — получить общую информацию по всем валютам (баланс, курсы, суммы в каждой валюте).
  * **POST** `/api/v1/amount/set/` — установить баланс для одной или нескольких валют.
  * **POST** `/api/v1/modify/` — изменить (прибавить/убавить) баланс валют.
* Автоматическое логирование операций и обновлений в консоль и в файл `app.log`.

## Установка

1. Клонировать репозиторий:

   ```bash
   git clone <URL_РЕПОЗИТОРИЯ>
   cd currency-service
   ```
2. Создать и активировать виртуальное окружение:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Linux/MacOS
   .venv\Scripts\activate    # Windows
   ```
3. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

## Конфигурация

Настройки приложения (`app/config.py`) можно переопределить через переменные окружения:

* **CURRENCIES** (по умолчанию `usd`, `eur`, `rub`)
* **RUN\_HOST** (по умолчанию `0.0.0.0`)
* **RUN\_PORT** (по умолчанию `8000`)
* **RUN\_COUNT\_WORKERS** (по умолчанию `4`)
* **FETCH\_URL** (URL API курсов, по умолчанию `https://www.cbr-xml-daily.ru/daily_json.js`)
* **FETCH\_TIMEOUT** (таймаут HTTP-запросов, по умолчанию `10`)
* **SCHEDULER\_PRINT\_SLEEP** (интервал логирования в консоль, мин, по умолчанию `1`)
* **LOGGER\_LOG\_FILE** (файл для логов, по умолчанию `app.log` в корне проекта)

## Запуск

```bash
python3 -m app.service \
  --rub 1000 \
  --usd 500 \
  --eur 300 \
  --period 10 \
  --debug true
```

* `--rub`, `--usd`, `--eur` — начальные балансы (можно задавать в любом порядке).
* `--period` — период обновления курсов в минутах (обязательный параметр).
* `--debug` — режим отладки (`true`/`false`, по умолчанию `false`).


## Примеры запросов

* **Получить баланс USD**:

  ```bash
  curl http://localhost:8000/api/v1/usd/get/
  ```
* **Получить общую информацию по всем валютам**:

  ```bash
  curl http://localhost:8000/api/v1/amount/get/
  ```
* **Установить баланс EUR**:

  ```bash
  curl -X POST http://localhost:8000/api/v1/amount/set/ \
       -H "Content-Type: application/json" \
       -d '{"eur": 120.5}'
  ```
* **Изменить баланс (добавить 20 USD, убрать 50 RUB)**:

  ```bash
  curl -X POST http://localhost:8000/api/v1/modify/ \
       -H "Content-Type: application/json" \
       -d '{"rub": -50, "usd": 20}'
  ```

## Структура проекта

```
currency-service/
├── app
│   ├── api         # REST-роуты
│   ├── core        # Бизнес-логика, планировщики, состояние
│   ├── schemas     # Pydantic модели запросов/ответов
│   └── utils       # Утилиты (логгер, CLI)
├── requirements.txt
├── .flake8
└── .gitignore
```