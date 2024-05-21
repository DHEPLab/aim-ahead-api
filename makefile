.PHONY: start
start: install run

.PHONY: install
install:
	pip3 install pipenv
	pipenv --python `which python3`
	pipenv install
	if [ ! -f .env ]; then cp .env.temp .env; fi 

.PHONY: run
run: install
		export PYTHONPATH=`pwd` && \
		docker-compose up -d db && \
		pipenv run python3 src/app.py \
	'

.PHONY: format
format: install
	pipenv run black src


.PHONY: lint
lint: install
	pipenv run flake8 src


.PHONY: test
test: install
	sh -c ' \
       	export TESTCONTAINERS_RYUK_DISABLED=true && \
       	export DOCKER_HOST=unix:///var/run/docker.sock && \
		pipenv run pytest tests\
	'

.PHONY: clean
clean:
	pipenv --rm
	docker stop postgres_container
