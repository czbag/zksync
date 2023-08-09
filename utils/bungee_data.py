import requests


def get_bungee_data():
    url = "https://refuel.socket.tech/chains"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["result"]
        return data
    return False
