# ClickHouse ETL Pipeline

Простой ETL-пайплайн: тянет курсы валют из публичного API, чистит через pandas, грузит в ClickHouse.

## Стек
- Python (requests, pandas, clickhouse-connect)
- ClickHouse
- Docker / docker-compose

## Архитектура
API (exchangerate-api.com) → extract.py → data/*.json → transform.py → pandas DataFrame → load.py → ClickHouse

## Запуск

1. Поднять ClickHouse:
docker-compose up -d

2. Установить зависимости:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Скопировать .env.example в .env и вписать свои значения:
cp .env.example .env

4. Запустить пайплайн:
python src/load.py

5. Проверить данные:
docker exec -it ch_server clickhouse-client --user default --password <пароль> --database analytics
SELECT * FROM exchange_rates LIMIT 10;