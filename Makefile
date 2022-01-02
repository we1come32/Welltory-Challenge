build:
	docker build -t we1come32/Welltory-Challenge .

run:
	docker run --name wc -d we1come32/Welltory-Challenge

stop:
	docker stop wc

clear:
	docker container rm wc
	docker image rm we1come32/Welltory-Challenge

logs:
	docker logs wc

start:
	docker start wc -p 8080:80

push:
	docker push we1come32/Welltory-Challenge

restart:
	make stop
	make clear
	make build
	make run
	make logs
