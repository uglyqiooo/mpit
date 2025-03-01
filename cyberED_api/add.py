import requests

# Добавить пароль и email
response = requests.post("http://127.0.0.1:8000/add_password")
print(response.json())