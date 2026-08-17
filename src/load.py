import os
from dotenv import load_dotenv
import clickhouse_connect
from transform import transform_rates

load_dotenv()

def get_client():
    return clickhouse_connect.get_client(
        host=os.getenv("CH_HOST"),
        port=int(os.getenv("CH_PORT")),
        username=os.getenv("CH_USER"),
        password=os.getenv("CH_PASSWORD"),
        database=os.getenv("CH_DATABASE")
    )

def create_table(client):
    client.command("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            currency String,
            rate Float64,
            base_currency String,
            date Date,
            loaded_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date, currency)
    """)
    print("Таблица exchange_rates готова")

def load_data(client, df):
    data = df[["currency", "rate", "base_currency", "date"]].values.tolist()
    client.insert(
        "exchange_rates",
        data,
        column_names=["currency", "rate", "base_currency", "date"]
    )
    print(f"Загружено {len(data)} строк в ClickHouse")

if __name__ == "__main__":
    client = get_client()
    create_table(client)
    df = transform_rates()
    load_data(client, df)