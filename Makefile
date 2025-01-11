build:
	docker-compose -f docker-compose.$(for).yml build

start:
	docker-compose -f docker-compose.$(for).yml up --force-recreate --remove-orphans