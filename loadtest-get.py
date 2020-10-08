from locust import HttpUser, task, between
import csv
import random

users = []
with open('user.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        users.append(row)

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def tast_get(self):
        cpf = users[random.randint(0, len(users))][2]
        self.client.get("/get/%s" % cpf)