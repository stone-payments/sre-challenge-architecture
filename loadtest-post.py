from locust import HttpUser, task, between
import csv

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
    def task_post(self):
        """ Task que efetua um post ao destino, usando o header """
        for userList in users:
            header={'Content-Type': 'application/xml',
            'User-Agent': 'locust',
            'nome' : userList[0],
            'sobrenome' : userList[1],
            'cpf' : userList[2],
            'bday' : userList[3] }

            self.client.post( "/post", headers=header )