from locust import HttpUser, TaskSet, between, task
import random

class SignUp(TaskSet):
    _url = "/api/v1/members"
    
    @task
    def sign_up(self):
        user_data = {
            "user_id": f"user{random.randint(0, 9999)}",
            "name": "테스트 사용자",
            "password": "password123",
            "email": f"user{random.randint(0000, 9999)}@example.com",
            "phone": f"010-{random.randint(0000, 9999)}-{random.randint(0000, 9999)}",
            "type": random.choice(["consumer", "vender"])
        }
        response = self.client.post(f"{self._url}/sign-up", json=user_data)

        if response.status_code == 201:
            print("회원 등록 완료:", user_data["user_id"])
        else:
            print("회원 등록 실패:", response.status_code, response.text)

class Test(HttpUser):
    tasks = [SignUp]
    wait_time = between(1, 5)