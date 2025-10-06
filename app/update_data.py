import requests
import psycopg2

import requests

BASE_URL = "http://localhost:8000"

# Получение кода станции по имени через API
def get_station_code(name: str):
    url = f"{BASE_URL}/stations"
    params = {"query": name}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"Ошибка запроса станций: {e}")
        return None

    # Предположим, что API возвращает список словарей: [{"code": "MOW", "name": "Москва"}, ...]
    codes = [station["code"] for station in data.get("stations", []) if name.lower() in station["name"].lower()]
    return codes if codes else None


if __name__ == "__main__":
    from_codes = get_station_code("Москва")
    to_codes = get_station_code("Санкт-Петербург")

    print("FROM:", from_codes)
    print("TO:", to_codes)



# Поиск минимальной цены
def fetch_prices(from_codes: list, to_codes: list):
    url = f"https://suggest.travelpayouts.com/search"

    for from_code in from_codes:
        for to_code in to_codes:
            params = {
                "service" : "tutu_trains",
                "term": from_code[0],
                "term2": to_code[0],
                "date" : "2025-10-07"
            }
            resp = requests.get(url, params=params, timeout=30)
            print(resp.status_code)
            print(resp.text)
            data = resp.json()
            
            prices = []

            for trip in data.get("trips", []):


                for category in trip.get("categories", []):
                    
                    price = category.get("price", {})
                    if price is not None:
                        prices.append(price)

    return min(prices) if prices else "Цены не найдены"




if __name__ == "__main__":
    from_code = get_station_code("Москва", True)
    to_code = get_station_code("Санкт-Петербург", False)
    

    print(fetch_prices(from_code, to_code))
