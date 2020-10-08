#Criar makefile para teste de carga

HOST=http://

test-up:
	apt -y install python3 python3-pip python3-venv;
	python3 -m venv testenv;
	. testenv/bin/activate;	pip install locust

get:
	. testenv/bin/activate;	locust -f loadtest-get.py --headless -u 1000 -r 100 --run-time 10m -H $(HOST)
post:
	. testenv/bin/activate;	locust -f loadtest-post.py --headless -u 2 -r 1 -H $(HOST)

run:
	ansible-playbook -i inventory.ini playbook.yml
clean:
	ansible-playbook -i inventory.ini clean.yml