from locust import HttpUser, TaskSet, between, events, task
from locust.clients import HttpSession
import random

class ReservationList(TaskSet):
    """
    locust -f get_reservations.py --host http://localhost:60003
    1. 로그인 후 토큰 생성
    2. 생성된 토큰으로 예약 목록 요청
    """

    @task
    def get_reservations(self):
        if hasattr(self.user, 'token'):
            params = {
                "skip": random.randint(0, 100),
                "limit": 30
            }
            headers = {
                "Authorization": self.user.token
            }

            response = self.client.get(
                "/api/v1/reservations", 
                headers=headers,
                params=params
            )

            if response.status_code == 200:
                print("예약 목록 요청 성공")
            else:
                print("예약 목록 요청 실패")
        else:
            print("토큰이 없습니다.")


class Test(HttpUser):
    tasks = [ReservationList]
    wait_time = between(1, 5)


@events.test_start.add_listener
def login(environment, **kwargs):
    if not environment.runner:
        return
        
    client = HttpSession(
        base_url="http://localhost:60000",
        request_event=environment.events.request,
        user=None
    )
    response = client.post(
        "http://localhost:60000/api/v1/members/sign-in",
        json={
            "user_id": "test2_id",
            "password": "password123",
            "type": "vendor"
        }
    )
    
    if response.status_code == 200:
        print("로그인 성공:", response.status_code, response.text)
        token = f"Bearer {response.json().get('access_token')}"
        environment.token = token
        Test.token = token
    else:
        print("로그인 실패:", response.status_code, response.text)
        environment.token = None
        Test.token = None