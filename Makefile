.PHONY: server check format


#################################################################################
# COMMANDS                                                                      #
#################################################################################
##RUN Docker
docker_server:
	docker-compose build
	docker-compose up

##Down Docker
docker_server_down:
	docker-compose down

##Run locally
server:
	python -m uvicorn API.main:app --reload

## Run linting checks
check:
	isort --check async_project tests
	black --check async_project tests
	flake8 async_project tests --max-line-length 120
	mypy async_project tests

format:
	isort API
	black API

