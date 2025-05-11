import requests
import json

# Базовый URL для API работ (Jobs)
API_BASE_URL = "http://127.0.0.1:5000/api/v2/jobs"


def print_response(response):
    print(f"Статус код: {response.status_code}")
    try:
        print("JSON ответ:")
        print(json.dumps(response.json(), indent=4))
    except json.JSONDecodeError:
        print("Ответ не в формате JSON")


def test_jobs_api():
    print("--- Демонстрация работы Jobs API ---")

    # 1. Получение списка всех работ
    print("\n1. Получение списка всех работ:")
    response = requests.get(API_BASE_URL)
    print_response(response)
    if response.status_code != 200:
        return

    # 2. Получение конкретной работы (предположим, что ID 1 существует)
    print("\n2. Получение работы с ID 1:")
    response = requests.get(f"{API_BASE_URL}/1")
    print_response(response)
    if response.status_code != 200:
        return

    # 3. Создание новой работы
    print("\n3. Создание новой работы:")
    new_job_data = {
        "job": "Тестирование REST API",
        "team_leader": 1,
        "work_size": 15,
        "collaborators": "2,3,4",
        "is_finished": False
    }
    response = requests.post(API_BASE_URL, data=new_job_data)  # Используем data=, а не json=
    print_response(response)
    if response.status_code != 201:  # Ожидаем код 201 (Created)
        return

    new_job_id = response.json().get("id")
    print(f"Создана работа с ID: {new_job_id}")

    # 4. Редактирование работы
    print("\n4. Редактирование работы (изменим job и is_finished):")
    update_data = {
        "job": "Тестирование REST API - ОБНОВЛЕНО",
        "is_finished": True
    }
    response = requests.put(f"{API_BASE_URL}/{new_job_id}", data=update_data)  # Используем data=
    print_response(response)
    if response.status_code != 200:
        return

    # 5. Удаление работы
    print("\n5. Удаление работы:")
    response = requests.delete(f"{API_BASE_URL}/{new_job_id}")
    print_response(response)
    if response.status_code != 204:  # Ожидаем код 204 (No Content)
        return

    print("\n--- Все операции выполнены ---")


if __name__ == "__main__":
    test_jobs_api()
