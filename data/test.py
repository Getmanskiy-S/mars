import requests
import json

# Базовый URL API для пользователей
API_BASE_URL = "http://127.0.0.1:5000/api/users"


def print_response(response):
    print(f"Статус код: {response.status_code}")
    try:
        print("JSON ответ:")
        print(json.dumps(response.json(), indent=4))
    except json.JSONDecodeError:
        print("Ответ не в формате JSON")


def test_user_api():
    print("--- Демонстрация работы User API ---")

    # 1. Получение списка всех пользователей
    print("\n1. Получение списка всех пользователей:")
    response = requests.get(API_BASE_URL)
    print_response(response)
    if response.status_code != 200:
        return  # Прекращаем выполнение, если произошла ошибка

    # 2. Получение конкретного пользователя (предположим, что ID 1 существует)
    print("\n2. Получение пользователя с ID 1:")
    response = requests.get(f"{API_BASE_URL}/1")
    print_response(response)
    if response.status_code != 200:
        return

    # 3. Создание нового пользователя
    print("\n3. Создание нового пользователя:")
    new_user_data = {
        "surname": "Иванов",
        "name": "Иван",
        "age": 30,
        "position": "Инженер",
        "speciality": "Программист",
        "address": "Марс, ул. Гагарина, 1",
        "email": "ivanov@mars.org"  # Уникальный email!
    }
    response = requests.post(API_BASE_URL, json=new_user_data)
    print_response(response)
    if response.status_code != 200:
        return

    new_user_id = response.json().get("id")
    print(f"Создан пользователь с ID: {new_user_id}")

    # 4. Редактирование пользователя
    print("\n4. Редактирование пользователя (изменим должность):")
    update_data = {
        "position": "Старший инженер"
    }
    response = requests.put(f"{API_BASE_URL}/{new_user_id}", json=update_data)
    print_response(response)
    if response.status_code != 200:
        return

    # 5. Удаление пользователя
    print("\n5. Удаление пользователя:")
    response = requests.delete(f"{API_BASE_URL}/{new_user_id}")
    print_response(response)
    if response.status_code != 204:
        return

    print("\n--- Все операции выполнены ---")


if __name__ == "__main__":
    test_user_api()
