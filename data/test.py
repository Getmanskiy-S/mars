import requests

BASE_URL = 'http://127.0.0.1:5000/api/jobs'  # Базовый URL API

def test_get_all_jobs():
    """Тестирование получения всех работ."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"Ожидался статус код 200, получен {response.status_code}"
    data = response.json()
    assert 'jobs' in data, "В ответе отсутствует ключ 'jobs'"
    print("Успешно получены все работы.")


def test_get_job_by_id_valid():
    """Тестирование получения работы по существующему ID."""
    response = requests.get(f'{BASE_URL}/1')
    assert response.status_code == 200, f"Ожидался статус код 200, получен {response.status_code}"
    data = response.json()
    assert 'jobs' in data, "В ответе отсутствует ключ 'jobs'"
    print("Успешно получена работа по ID.")


def test_get_job_by_id_invalid():
    """Тестирование получения работы по несуществующему ID."""
    response = requests.get(f'{BASE_URL}/101')
    assert response.status_code == 404, f"Ожидался статус код 404, получен {response.status_code}"
    data = response.json()
    assert 'error' in data, "В ответе отсутствует ключ 'error'"
    print("Успешно обработан запрос с несуществующим ID.")


def test_get_job_by_id_type_error():
    """Тестирование получения работы по ID, являющемуся строкой (некорректный тип)."""
    response = requests.get(f'{BASE_URL}/error')
    assert response.status_code == 404, f"Ожидался статус код 404, получен {response.status_code}"
    data = response.json()
    assert 'error' in data, "В ответе отсутствует ключ 'error'"
    print("Успешно обработан запрос с некорректным типом ID.")


def test_create_job_valid():
    """Тестирование успешного создания новой работы."""
    new_job = {
        'job': 'Исследование поверхности Марса',
        'team_leader': 1,
        'work_size': '100',
        'collaborators': '2, 3',
        'is_finished': False
    }
    response = requests.post(BASE_URL, json=new_job)
    assert response.status_code == 200, f"Ожидался статус код 200, получен {response.status_code}"
    data = response.json()
    assert 'id' in data, "В ответе отсутствует ключ 'id'"
    print("Успешно создана новая работа.")

    # Проверяем, что работа действительно добавлена, получая список всех работ
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"Ожидался статус код 200, получен {response.status_code}"
    all_jobs = response.json()['jobs']
    new_job_exists = False
    for job in all_jobs:
        if job['job'] == new_job['job'] and job['team_leader'] == new_job['team_leader']:
            new_job_exists = True
            break
    assert new_job_exists, "Созданная работа не найдена в списке всех работ."


def test_create_job_missing_field():
    """Тестирование создания работы с отсутствующим обязательным полем (team_leader)."""
    invalid_job = {
        'job': 'Некорректная работа',
        'work_size': '50',
        'collaborators': '4, 5',
        'is_finished': True
    }
    response = requests.post(BASE_URL, json=invalid_job)
    assert response.status_code == 404, f"Ожидался статус код 404, получен {response.status_code}"
    data = response.json()
    assert 'error' in data, "В ответе отсутствует ключ 'error'"
    print("Успешно обработан запрос с отсутствующим полем.")


def test_create_job_empty_request():
    """Тестирование создания работы с пустым запросом."""
    response = requests.post(BASE_URL, json={})
    assert response.status_code == 404, f"Ожидался статус код 404, получен {response.status_code}"
    data = response.json()
    assert 'error' in data, "В ответе отсутствует ключ 'error'"
    print("Успешно обработан запрос с пустым телом запроса.")


def test_create_job_invalid_data_type():
    """Тестирование создания работы с некорректным типом данных (work_size - строка вместо числа)."""
    invalid_job = {
        'job': 'Работа с некорректным типом данных',
        'team_leader': 1,
        'work_size': 'abc',  # Должно быть числом
        'collaborators': '6, 7',
        'is_finished': False
    }
    response = requests.post(BASE_URL, json=invalid_job)
    assert response.status_code == 404, f"Ожидался статус код 404, получен {response.status_code}"
    data = response.json()
    assert 'error' in data, "В ответе отсутствует ключ 'error'"
    print("Успешно обработан запрос с некорректным типом данных.")


# Запуск тестов
test_get_all_jobs()
test_get_job_by_id_valid()
test_get_job_by_id_invalid()
test_get_job_by_id_type_error()
test_create_job_valid()
test_create_job_missing_field()
test_create_job_empty_request()
test_create_job_invalid_data_type()

print("Все тесты завершены.")