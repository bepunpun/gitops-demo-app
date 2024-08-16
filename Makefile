IMAGE   ?= gitops-demo-app
GIT_SHA := $(shell git rev-parse --short HEAD)

.PHONY: test build run

.venv/bin/pytest: requirements-dev.txt
	python3 -m venv .venv
	.venv/bin/pip install -q -r requirements-dev.txt

test: .venv/bin/pytest
	.venv/bin/pytest -q

build:
	docker build --build-arg GIT_SHA=$(GIT_SHA) -t $(IMAGE):$(GIT_SHA) .

run: build
	docker run --rm -p 8000:8000 -e APP_ENV=local $(IMAGE):$(GIT_SHA)
