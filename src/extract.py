import requests
import json
from datetime import datetime

def extract_rates():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    response.raise_for_status()  # если ошибка - упадём тут, а не молча
    data = response.json()
    
    # сохраняем сырой ответ на диск, чтоб был "снапшот" на случай отладки
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"data/raw_rates_{timestamp}.json"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Данные сохранены: {filepath}")
    return data

if __name__ == "__main__":
    extract_rates()