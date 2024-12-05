from locust import HttpUser, TaskSet, between, task
import random

class SignIn(TaskSet):
    _url = "/api/v1/members"

    @task
    def sign_in(self):
        user_data = {
            "user_id": f"user{random.randint(0, 9999)}",
            "password": "password123",
            "type": random.choice(["consumer", "vender"])
        }
        response = self.client.post(f"{self._url}/sign-in", json=user_data)
        if response.status_code == 200:
            if not self._access_token:
                self._access_token = response.json().get("access_token")

class Test(HttpUser):
    tasks = [SignIn]
    wait_time = between(1, 5)