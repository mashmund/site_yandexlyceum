from requests import post, get

print(get('http://localhost:8008/api/jobs').json())

print(get('http://localhost:8008/api/jobs/1').json())

print(get('http://localhost:8008/api/jobs/1999').json())

print(get('http://localhost:8008/api/jobs/abc').json())

print(post('http://localhost:8008/api/jobs').json())
print(post('http://localhost:8008/api/jobs',
           json={'job': 'installing a long-distance communication antenna', 'team_leader': 1, 'work_size': 5,
                 'collaborators': '6, 3', 'is_finished': True}).json())
