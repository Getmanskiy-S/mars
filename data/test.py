import requests
import json

# ID работы, которую нужно отредактировать.  ОБЯЗАТЕЛЬНО ИЗМЕНИТЕ!
JOB_ID_TO_EDIT = 1

# URL API
API_BASE_URL = "http://127.0.0.1:5000/api/jobs"

# Данные, которые будут отправлены для обновления работы.  ОБЯЗАТЕЛЬНО ИЗМЕНИТЕ!
# В этом примере изменяем только название работы и исполнителей.
UPDATE_DATA = {
    'job': 'Обновленное название работы',
    'collaborators': '5, 6, 7'
    # Вы можете добавить другие поля, которые нужно обновить
    # Например:
    # 'work_size': 20,
    # 'is_finished': True
}

# Формируем URL для PUT запроса
EDIT_URL = f"{API_BASE_URL}/{JOB_ID_TO_EDIT}"

print(f"Отправляем PUT запрос на URL: {EDIT_URL}")
print(f"Данные для обновления: {json.dumps(UPDATE_DATA, indent=4)}")  # Выводим JSON для наглядности

# Отправляем PUT запрос
response = requests.put(EDIT_URL, json=UPDATE_DATA)

print(f"Получен статус код: {response.status_code}")

# Проверяем статус код
if response.status_code == 200:
    print("Работа успешно отредактирована.")
    print("JSON ответ сервера (обновленная работа):")
    print(json.dumps(response.json(), indent=4))  # Красиво выводим JSON
elif response.status_code == 404:
    print("Ошибка: Работа с указанным ID не найдена.")
else:
    print(f"Произошла ошибка. Статус код: {response.status_code}")
    try:
        print(f"Сообщение об ошибке: {response.json()}")  # Пытаемся вывести сообщение об ошибке в JSON формате
    except json.JSONDecodeError:
        print("Не удалось декодировать JSON из ответа сервера.")

print("\n--- Важно ---")
print("1. Убедитесь, что Flask-приложение запущено.")
print("2. Убедитесь, что работа с указанным JOB_ID_TO_EDIT существует в базе данных.")
print("3. Отредактируйте UPDATE_DATA, указав нужные значения для обновления.")
print("4. Проверьте логи Flask-приложения для получения дополнительной информации об ошибках.")
