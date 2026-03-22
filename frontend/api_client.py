import requests
from typing import Optional, Dict
import os

BASE_URL = os.getenv("API_URL", "http://backend:8000")

class APIClient:
    def __init__(self):
        self.token: Optional[str] = None
        self.username: Optional[str] = None

    def _get_headers(self) -> dict:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def register(self, username, email, password) -> Dict:
        res = requests.post(f"{BASE_URL}/users/", json={"username": username, "email": email, "password": password})
        return res.json(), res.status_code

    def login(self, username, password) -> Dict:
        res = requests.post(f"{BASE_URL}/login", data={"username": username, "password": password})
        data = res.json()
        if res.status_code == 200:
            self.token = data.get("access_token")
            self.username = username
        return data, res.status_code

    def logout(self):
        self.token = None
        self.username = None

    def get_posts(self, search=""):
        res = requests.get(f"{BASE_URL}/posts/", headers=self._get_headers(), params={"search": search})
        if res.status_code == 200:
            return res.json()
        print(f"Failed to fetch posts: {res.text}")
        return []

    def create_post(self, title, content):
        res = requests.post(f"{BASE_URL}/posts/", json={"title": title, "content": content}, headers=self._get_headers())
        return res.json(), res.status_code

    def update_post(self, post_id, title, content):
        res = requests.put(f"{BASE_URL}/posts/{post_id}", json={"title": title, "content": content}, headers=self._get_headers())
        return res.json(), res.status_code

    def delete_post(self, post_id):
        res = requests.delete(f"{BASE_URL}/posts/{post_id}", headers=self._get_headers())
        return res.status_code

    def vote(self, post_id, dir_value):
        res = requests.post(f"{BASE_URL}/posts/vote", json={"post_id": post_id, "dir": dir_value}, headers=self._get_headers())
        return res.json(), res.status_code

client = APIClient()
