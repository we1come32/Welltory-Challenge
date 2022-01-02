build:
	docker build -t we1come32/welltory-challenge:latest .

run:
	docker run --name wc -d we1come32/welltory-challenge -p 80:8080

stop:
	docker stop wc

clear:
	docker container rm wc
	docker image rm we1come32/welltory-challenge

logs:
	docker logs wc

start:
	docker start wc

push:
	docker push we1come32/welltory-challenge

restart:
	make stop
	make clear
	make build
	make run
	make logs
