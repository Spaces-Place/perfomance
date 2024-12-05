
import json
import random
from locust import HttpUser, TaskSet, between, events, task
from locust.clients import HttpSession
import faker


fake = faker.Faker('ko-KR')

class Space(TaskSet):
    """
    locust -f post_space.py --host http://localhost:60001
    1. 로그인 후 토큰 생성
    2. 생성된 토큰으로 공간 생성 요청
    """

    @task
    def create_space(self):
        if hasattr(self.user, 'token'):
            # 랜덤한 공간 등록 데이터 생성
            user_id = 'test2_id'
            space_type = random.choice(['PLAYING', 'PARTY', 'DANCE', 'KARAOKE', 'STUDIO', 'CAMPING', 'GYM', 'OFFICE', 'ACCOMMODATION', 'KITCHEN', 'STUDYROOM'])
            space_name = fake.catch_phrase()
            capacity = random.randint(1, 20)
            space_size = random.randint(10, 500)
            usage_unit = random.choice(['TIME', 'DAY'])
            unit_price = random.randint(10000, 100000)
            amenities = random.sample(['parking', 'wifi', 'air_conditioning', 'heating', 'kitchen'], k=random.randint(1, 5))
            description = fake.sentence()
            content = fake.paragraph()
            location = {
                'sido': fake.city(),
                'address': fake.address(),
                'coordinates': [round(random.uniform(126.0, 129.0), 6), round(random.uniform(33.0, 38.0), 6)]
            }
            weekdays = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
            operating_hour = [
                {
                    'day': day,
                    'open': f"{random.randint(6, 10)}:00",
                    'close': f"{random.randint(17, 23)}:00"
                }
                for day in weekdays
            ]
            
            images = ['images/camping1.jpg', 'images/map.png']

            form_data = {
                'user_id': user_id,
                'space_type': space_type,
                'space_name': space_name,
                'capacity': capacity,
                'space_size': space_size,
                'usage_unit': usage_unit,
                'unit_price': unit_price,
                'amenities': amenities,
                'description': description,
                'content': content,
                'location': json.dumps(location),
                'operating_hour': json.dumps(operating_hour),
                'is_operate': True,
            }

            files = []
            for image_path in images:
                with open(f'./{image_path}', 'rb') as img_file:
                    files.append(('images', (image_path, img_file.read())))

            headers = {
                "Authorization": self.user.token
            }

            response = self.client.post(
                '/api/v1/spaces', 
                data=form_data, 
                files=files, 
                headers = headers
            )

            if response.status_code == 201:
                print("공간 생성 완료")
            else:
                print("공간 생성 실패:", response.status_code, response.text)

class Test(HttpUser):
    tasks = [Space]
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