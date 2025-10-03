import psycopg2

def get_station_code(name: str):
    conn = psycopg2.connect(
        dbname="train_tickets",
        user="root_ticket",
        password="root_ticket",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    query = "SELECT from_code FROM stations WHERE from_name = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None

print(get_station_code("Москва"))