import requests

credentials = {
        'name': 'user',
        'password': 'password'
        }
res = requests.post('http://localhost:8000/login', json=credentials)
print (res.text)