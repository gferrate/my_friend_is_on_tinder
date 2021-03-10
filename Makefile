update:
	docker-compose build
	docker-compose up -d
	docker system prune -a -f

build:
	docker-compose build

run:
	docker-compose up -d

clean:
	docker system prune -a -f
