from locust import HttpLocust, TaskSet, task,  between
from datetime import datetime
import json
import random

class UserBehavior(TaskSet):
    def __init__(self):
        self.user_no = 1;
        super().__init__(self)

    def on_start(self):
        user = {"username": "locust"+str(user_no), "password": "1234567890123456789012345678901234567890"}
        self.user_no = self.user_no + 1
        self.client.put('/api/v1/users', data=json.dumps(user), headers={'Content-Type': 'application/json'})
        print("on start added user")

    def add_ride(self):
        time = datetime.now() + datetime.timedelta(days = 1)
        ride = {"created_by":"locust", "timestamp":time.strftime("%d-%m-%Y:%S-%M-%H"),"source":"2", "destination":"4"}
        self.client.post('/api/v1/rides', data=json.dumps(ride), headers={'Content-Type': 'application/json'})
        print("on setup created ride")

    def on_stop(self):
        self.client.delete('/api/v1/users/{username}'.format(username="locust"+str(user_no))
        self.user_no = self.user_no - 1
        print("on stop deleted user")


    def create_ride(self):
        time = datetime.now() + datetime.timedelta(days = 1)
        ride = {"created_by":"locust", "timestamp":time.strftime("%d-%m-%Y:%S-%M-%H"),"source":"2", "destination":"4"}
        self.client.post('/api/v1/rides', data=json.dumps(ride), headers={'Content-Type': 'application/json'})

    def join_ride(self):
        username = {"username": "locustio"}
        self.client.post('/api/v1/rides', data=json.dumps(username), headers={'Content-Type': 'application/json'})

    @task
    def index(self):
        self.client.get('/cc')
        print("/cc")

    @task
    def list_ride_details(self):
        self.client.get("/api/v1/rides/1")
        print("/api/v1/rides/1")

    @task
    def list_rides(self):
        self.client.get('/api/v1/rides?source={source}&destination={destination}'.format(source=2,destination=4))
        print("/api/v1/rides?")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(1, 5)

