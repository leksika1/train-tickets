import requests
import psycopg2

# Получение кода станции по имени
def get_station_code(name: str, flag_from_to: bool):
    conn = psycopg2.connect(
        dbname="train_tickets",
        user="root_ticket",
        password="root_ticket",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    if flag_from_to:
        query = "Select distinct(from_code) FROM stations WHERE from_name ilike %s "
    else:
        query = "Select distinct(to_code) FROM stations WHERE to_name ilike %s "


    cursor.execute(query, (name,))
    result = cursor.fetchall()

    conn.close()

    if result:
        return result
    else:
        return None


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
