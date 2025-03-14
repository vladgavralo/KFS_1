import requests

BASE_URL = "http://127.0.0.1:8000"

def request_with_error_handling(request_func, *args, **kwargs):
    """ . """
    try:
        response = request_func(*args, **kwargs)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            print(f"Помилка: {response.json().get('detail', '!')}")
        elif response.status_code == 404:
            print(f" Попередження: {response.json().get('detail', 'Дані не знайдено')}")
        else:
            print(f" Невідома помилка: {response.status_code} {response.text}")
    except requests.exceptions.ConnectionError:
        print(" Помилка: сервер недоступний. Переконайтеся, що FastAPI запущено.")
    except requests.exceptions.RequestException as e:
        print(f" Помилка мережі: {e}")
    return None

def add_meter():
    meter_number = input("Введіть номер лічильника: ")
    owner_name = input("Введіть ім'я власника: ")
    response = request_with_error_handling(requests.post, f"{BASE_URL}/add_meter", json={
        "meter_number": meter_number,
        "owner_name": owner_name
    })
    if response:
        print(response)

def add_reading():
    meter_id = int(input("Введіть ID лічильника: "))
    day_kwh = float(input("Введіть денне споживання (кВт): "))
    night_kwh = float(input("Введіть нічне споживання (кВт): "))
    response = request_with_error_handling(requests.post, f"{BASE_URL}/add_reading", json={
        "meter_id": meter_id,
        "day_kwh": day_kwh,
        "night_kwh": night_kwh
    })
    if response:
        print(response)

def get_history():
    meter_id = int(input("Введіть ID лічильника: "))
    response = request_with_error_handling(requests.get, f"{BASE_URL}/history", params={"meter_id": meter_id})
    if response:
        print(response)

def update_tariffs():
    day_rate = float(input("Введіть новий тариф для денного споживання (грн/кВт): "))
    night_rate = float(input("Введіть новий тариф для нічного споживання (грн/кВт): "))
    response = request_with_error_handling(requests.put, f"{BASE_URL}/update_tariffs", json={
        "day_rate": day_rate,
        "night_rate": night_rate
    })
    if response:
        print(response)

def export_history():
    meter_id = int(input("Введіть ID лічильника: "))
    response = request_with_error_handling(requests.get, f"{BASE_URL}/export_history", params={"meter_id": meter_id})
    if response:
        filename = f"history_{meter_id}.csv"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f" Історію успішно збережено у файл: {filename}")

def main():
    while True:
        print("\nВиберіть дію:")
        print("1. Додати новий лічильник")
        print("2. Додати показання лічильника")
        print("3. Отримати історію споживання")
        print("4. Оновити тарифи")
        print("5. Експортувати історію в CSV")
        print("6. Вихід")
        
        choice = input("Введіть номер дії: ")
        
        if choice == "1":
            add_meter()
        elif choice == "2":
            add_reading()
        elif choice == "3":
            get_history()
        elif choice == "4":
            update_tariffs()
        elif choice == "5":
            export_history()
        elif choice == "6":
            print("Вихід із програми.")
            break
        else:
            print(" Некорректный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()
