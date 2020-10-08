from locust import HttpUser, task, between
import csv
import random

#Carrega a lista de clientes
users = []
with open('user.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        users.append(row)

class QuickstartUser(HttpUser):
    """ Esta classe inicia a conexao com o destino """
    wait_time = between(1, 2)

    @task
    def tast_get(self):
        """ Task que efetua um get ao destino """
        cpf = users[random.randint(0, len(users))][2]
        self.client.get("/get/%s" % cpf)