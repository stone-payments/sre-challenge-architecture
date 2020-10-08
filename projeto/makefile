WORKDIR=/opt/projeto/docker
run: create-net create-containers
clean: clean-containers clean-images

EXISTAPI := $(shell docker network list|awk '{print $$2}'|grep api)

create-net:
ifeq ($(EXISTAPI), apinet)
	docker network rm apinet
endif
	docker network create apinet

create-postgres:
	docker run --hostname postgres --name postgres --network apinet -d psql
	sleep 4
	docker exec -it postgres psql -U postgres -f /opt/db/stone.sql
	docker exec -it postgres sed -e 's/max_connections = 100/max_connections = 1000/g' -i /var/lib/postgresql/data/postgresql.conf
	docker stop postgres
	docker start postgres

#PSQL := $(shell docker ps|grep postgres|wc -l)
#create-postgres-db:
#ifeq ($(PSQL), 1)
#else
#	break
#endif

#create-containers: build-images create-postgres create-postgres-db
create-containers: build-images create-postgres
	docker run --hostname redis --name redis --network apinet -d redis
	docker run --hostname stoneapi1 --name stoneapi1 --network apinet -d stoneapi
	docker run --hostname stoneapi2 --name stoneapi2 --network apinet -d stoneapi
	docker run --ulimit nofile=90000:90000 --hostname nginx --name nginx -p 80:80 --network apinet -d nginx

build-images:
	docker pull redis
	docker build -t psql -f $(WORKDIR)/postgres/Dockerfile .
	docker build -t stoneapi -f $(WORKDIR)/stoneapi/Dockerfile .
	docker build -t nginx -f $(WORKDIR)/nginx/Dockerfile .

CMD_IMAGE_RM=docker image rm
clean-img-db:
	$(CMD_IMAGE_RM) psql
clean-img-api:
	$(CMD_IMAGE_RM) stoneapi
clean-img-nginx:
	$(CMD_IMAGE_RM) nginx
clean-img-redis:
	$(CMD_IMAGE_RM) redis

CMD_CONTAINER_RM=docker rm
CMD_CONTAINER_STOP=docker stop
clean-c-db:
	$(CMD_CONTAINER_STOP) postgres
	$(CMD_CONTAINER_RM) postgres
clean-c-api:
	$(CMD_CONTAINER_STOP) stoneapi1
	$(CMD_CONTAINER_RM) stoneapi1
	$(CMD_CONTAINER_STOP) stoneapi2
	$(CMD_CONTAINER_RM) stoneapi2
clean-c-nginx:
	$(CMD_CONTAINER_STOP) nginx
	$(CMD_CONTAINER_RM) nginx
clean-c-redis:
	$(CMD_CONTAINER_STOP) redis
	$(CMD_CONTAINER_RM) redis

clean-images: clean-img-db clean-img-api clean-img-nginx clean-img-redis
clean-containers: clean-c-db clean-c-api clean-c-nginx clean-c-redis

clean-db: clean-c-db clean-img-db
clean-api: clean-c-api clean-img-api
clean-nginx: clean-c-nginx clean-img-nginx
clean-redis: clean-c-redis clean-img-redis
