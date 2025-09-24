import requests
import psycopg2
from datetime import datetime, timedelta

DB_CONFIG = {
    "dbname": "tickets",
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": 5432
}


def get_station_code(name: str):
    url = "https://ticket.rzd.ru/api/v1/suggests"
    params = {"stationName": name}
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data:
        return data[0]["stationCode"]
    return None

def fetch_prices(from_code: str, to_code: str, date: str):
    url = "https://ticket.rzd.ru/api/v1/search/"
    params = {"from": from_code, "to": to_code, "date": date}
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    prices = []
    for train in data.get("trains", []):
        for car in train.get("cars", []):
            prices.append(car["tariff"]["value"])

    return min(prices) if prices else None

def save_price(date: str, from_city: str, to_city: str, price: int):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO prices (date, from_city, to_city, price, updated_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (date, from_city, to_city, price, datetime.now()))

    conn.commit()
    cur.close()
    conn.close()

def update_route(from_city: str, to_city: str):
    from_code = get_station_code(from_city)
    to_code = get_station_code(to_city)
    if not from_code or not to_code:
        print("Не удалось найти коды станций")
        return

    start = datetime.now()
    for i in range(30):  # обновляем на месяц вперёд
        day = start + timedelta(days=i)
        date = day.strftime("%Y-%m-%d")
        price = fetch_prices(from_code, to_code, date)
        if price:
            save_price(date, from_city, to_city, price)
            print(f"✅ {date}: {from_city}–{to_city} = {price} руб.")
        else:
            print(f"⚠ {date}: данных нет")

if __name__ == "__main__":
    update_route("Москва", "Казань")
