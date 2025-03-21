from requests import get, post, delete

print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/1').json())
print(get('http://localhost:5000/api/v2/users/10').json())

print(post('http://localhost:5000/api/v2/users', json={}).json())  # нет данных
print(post('http://localhost:5000/api/v2/users', json={'name': 'Filya', 'surname': 'Ivanova'}).json())  # не все поля

print(post('http://localhost:5000/api/v2/users',
           json={'name': 'Filya', 'surname': 'Ivanova', 'age': 25, 'address': 'modul_2', 'email': 'fil@ya.ru',
                 'speciality': 'doctor', 'hashed_password': 'fox', 'position': '1'}).json())

print(get('http://localhost:5000/api/v2/users').json())
print(delete('http://localhost:5000/api/v2/users/10').json())
print(delete('http://localhost:5000/api/v2/users/2').json())

print(get('http://localhost:5000/api/v2/users').json())
