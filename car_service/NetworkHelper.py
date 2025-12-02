import requests
from requests.auth import HTTPBasicAuth


class NetworkHelper:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password)
        self.headers = {
            'Content-Type': 'application/json'
        }

    def get_teams(self):
        url = f"{self.base_url}/teams/"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def get_team_by_id(self, team_id):
        url = f"{self.base_url}/teams/{team_id}/"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def create_team(self, data):
        url = f"{self.base_url}/teams/"
        response = requests.post(url, json=data, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def update_team(self, team_id, data):
        url = f"{self.base_url}/teams/{team_id}/"
        response = requests.put(url, json=data, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def delete_team(self, team_id):
        url = f"{self.base_url}/teams/{team_id}/"
        response = requests.delete(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.status_code == 204

    def get_drivers(self):
        url = f"{self.base_url}/drivers/"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def get_driver_by_id(self, driver_id):
        url = f"{self.base_url}/drivers/{driver_id}/"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def create_driver(self, data):
        url = f"{self.base_url}/drivers/"
        response = requests.post(url, json=data, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def update_driver(self, driver_id, data):
        url = f"{self.base_url}/drivers/{driver_id}/"
        response = requests.put(url, json=data, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def delete_driver(self, driver_id):
        url = f"{self.base_url}/drivers/{driver_id}/"
        response = requests.delete(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.status_code == 204
