build:
	docker build -t order-book:latest .

run:
	docker run -p 8000:8000 -it order-book:latest

show:
	docker ps -a

stop:
	docker stop $$(docker ps -a)

remove:
	docker rm $$(docker ps -a -f status=exited -q)
