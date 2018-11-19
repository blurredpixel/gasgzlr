from locust import HttpLocust, TaskSet

def load(l):
    l.client.get("/")

def newuser (l):
    l.client.get("/login")

class UserBehavior(TaskSet):
    tasks={newuser:2}
    def on_start(self):
        load(self)
    def on_stop(self):
        load(self)
class Websiteuser(HttpLocust):
    task_set=UserBehavior
    min_wait=5000
    max_wait=9000