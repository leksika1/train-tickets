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
