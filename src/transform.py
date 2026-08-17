import pandas as pd
import json
import glob
import os

def transform_rates():
    # находим самый свежий файл в data/
    files = glob.glob("data/raw_rates_*.json")
    latest_file = max(files, key=os.path.getctime)
    
    with open(latest_file, "r") as f:
        data = json.load(f)
    
    # data выглядит так: {"base": "USD", "date": "...", "rates": {"EUR": 0.9, "RUB": 95.2, ...}}
    rates = data["rates"]
    base_currency = data["base"]
    date = data["date"]
    
    # превращаем словарь в таблицу: currency | rate
    df = pd.DataFrame(list(rates.items()), columns=["currency", "rate"])
    df["base_currency"] = base_currency
    df["date"] = date
    
    # приводим типы, чтоб не было сюрпризов при загрузке в ClickHouse
    df["rate"] = df["rate"].astype(float)
    df["date"] = pd.to_datetime(df["date"])
    
    print(f"Обработано {len(df)} валют из файла {latest_file}")
    print(df.head())
    
    return df

if __name__ == "__main__":
    transform_rates()