from locust import HttpLocust, TaskSet, task,  between
import requests
from datetime import datetime, timedelta
import json
import random

count = 0
ride_no = 0
source_list = list(range(1,6))
destination_list = list(range(6,11))
day_list = list(range(1,10))

class UserBehavior(TaskSet):

    def on_start(self):
        global count,ride_no
        self.client.post("/api/v1/db/write", data= json.dumps({"collection":"Ride", "jsonobj" : {} , "action":"delete"}),headers={'Content-Type': 'application/json'})
        user = {"username": "locust"+str(count), "password": "1234567890123456789012345678901234567890"}
        self.client.put('/api/v1/users', data=json.dumps(user), headers={'Content-Type': 'application/json'})
        print("on start added user")
        time = datetime.now() + timedelta(days = random.choice(day_list))
        ride = {"created_by":"locust"+str(count), "timestamp":time.strftime("%d-%m-%Y:%S-%M-%H"),"source":random.choice(source_list), "destination":random.choice(destination_list)}
        count += 1
        ride_no += 1
        print("ride: ",json.dumps(ride))
        self.client.post('/api/v1/rides', data=json.dumps(ride), headers={'Content-Type': 'application/json'})
        print("on setup created ride")

    def on_stop(self):
        global count
        count -= 1
        self.client.delete('/api/v1/users/{username}'.format(username="locust"+str(count)))
        print("on stop deleted user")

    @task(3)
    def create_ride(self):
        global ride_no
        ride_no += 1
        time = datetime.now() + timedelta(days = random.choice(day_list))
        ride = {"created_by":"locust"+str(random.choice(list(range(count)))), "timestamp":time.strftime("%d-%m-%Y:%S-%M-%H"),"source":str(random.choice(source_list)), "destination":str(random.choice(destination_list))}
        self.client.post('/api/v1/rides', data=json.dumps(ride), headers={'Content-Type': 'application/json'})

    @task(2)
    def delete_ride(self):
        global ride_no
        if(ride_no != 0):
            ride_list = list(range(1,ride_no+1))
            self.client.delete('/api/v1/rides/{rideId}'.format(rideId = random.choice(ride_list)))
            ride_no -= 1

    @task(1)
    def join_ride(self):
        username = {"username": "locust"+str(random.choice(list(range(count))))}
        self.client.post('/api/v1/rides', data=json.dumps(username), headers={'Content-Type': 'application/json'})

    @task(1)
    def index(self):
        self.client.get('/cc')
        print("/cc")

    @task(2)
    def list_ride_details(self):
        ride_list = list(range(1,ride_no+1))
        self.client.get("/api/v1/rides/"+str(random.choice(ride_list)))
        print("/api/v1/rides/ride_no")

    @task(2)
    def list_rides(self):
        self.client.get('/api/v1/rides?source={source}&destination={destination}'.format(source=str(random.choice(source_list)),destination=str(random.choice(destination_list))))
        print("/api/v1/rides?")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(1, 5)

