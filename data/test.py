from requests import get, post

print(get('http://127.0.0.1:5000/api/jobs').json())
print(get('http://127.0.0.1:5000/api/jobs/1').json())
print(get('http://127.0.0.1:5000/api/jobs/101').json())
print(get('http://127.0.0.1:5000/api/jobs/error').json())
print(get('http://127.0.0.1:5000/api/jobs/error').json())
print(post('http://localhost:5000/api/jobs',
           json={'job': 'Название',
                 'team_leader': 1,
                 'work_size': 5,
                 'collaborators': '2, 3',
                 'is_finished': False}).json())