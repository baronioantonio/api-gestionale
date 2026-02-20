import requests

url = "http://127.0.0.1:5000/clienti"

r = requests.post(url, json={
    "nome": "Test Python",
    "email": "test@api.it",
    "telefono": "999999"
})

print(r.status_code)
print(r.json())