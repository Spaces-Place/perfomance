import random
from locust import HttpUser, TaskSet, between, task

class Space(TaskSet):
    _url = "/api/v1/spaces"
    @task
    def get_spaces(self):
        # GET ?skip=60&limit=30이면 61~90 가져옴
        params = {
            "skip": random.randint(0, 100), # 0~100까지
            "limit": 30  # 한 번에 30개씩 요청
        }

        response = self.client.get(f"{self._url}", params=params)

        if response.status_code == 200:
            # print("공간 조회 완료:", response.json())
            print("공간 조회 완료:")
        else:
            print("공간 조회 실패:", response.status_code, response.text)


class Test(HttpUser):
    tasks = [Space]
    wait_time = between(1, 5)